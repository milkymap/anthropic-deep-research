import json 
from openai import OpenAI
from anthropic import Anthropic

from anthropic.types import RawMessageStreamEvent
from openai.types.chat import ChatCompletion, ChatCompletionChunk, ParsedChatCompletion

from concurrent.futures import ThreadPoolExecutor

from .types import Role, ChatMessage, StopReason
from .definitions import SystemPromptDefinitions, deep_iterattive_web_search_tool, simple_web_search_tool
from typing import List, Tuple, Dict, Any, Optional, Iterable

from operator import itemgetter, attrgetter

from .log import logger 
from contextlib import suppress

class AgentLoop:
    def __init__(self, openai_api_key:str, anthropic_api_key:str):
        self.openai_api_key = openai_api_key
        self.anthropic_api_key = anthropic_api_key
    
    def simple_web_search(self, expanded_queries:str, search_context_size:str) -> List[Dict]:
        
        openai_client = OpenAI(api_key=self.openai_api_key)
        def make_search(openai_client:OpenAI, query:str, search_context_size:str) -> str:
            try:
                completion_res:ChatCompletion = openai_client.chat.completions.create(
                    model='gpt-4o-mini-search-preview',
                    max_tokens=4096,
                    web_search_options={
                        'search_context_size': search_context_size
                    },
                    messages=[ChatMessage(role=Role.USER, content=query)]
                ) 
                search_result = completion_res.choices[0].message.content
                search_result = f'query:{query}\n###\nresult:{search_result}'
                logger.info(f'query {query} was successful')
                return search_result
            except Exception as e:
                logger.error(f'query {query} -> error: {e}')
                return f'query:{query} -> result: error: {e}'
        
        nb_queries = len(expanded_queries)
        with ThreadPoolExecutor(max_workers=nb_queries) as executor:
            futures = executor.map(lambda query: make_search(openai_client, query, search_context_size), expanded_queries)
            search_results = list(futures)
        return [
            {
                'type': 'text',
                'text': '\n\n---$$$---\n\n'.join(search_results)
            }
        ]
    
    def deep_iterative_web_search(self, query:str, user_contraints:str, task_complexity:str, max_iterations:int=1) -> List[Dict]:
        budget_tokens = 1024 
        match task_complexity:
            case 'medium':
                budget_tokens = 2048
            case 'high':
                budget_tokens = 4096
        
        user_message_content = f'query: {query}\ntask_complexity: {task_complexity}\nuser_contraints: {user_contraints}'
        conversation_history = [ChatMessage(role=Role.USER, content=user_message_content)]
        stop_reason = StopReason.TOOL_USE

        counter = 0
        while stop_reason == StopReason.TOOL_USE:
            if counter > max_iterations:
                break

            completion_res:Iterable[RawMessageStreamEvent] = self.handle_conversation(
                system=SystemPromptDefinitions.DEEP_ITERATIVE_WEB_SEARCH.format(max_iterations=max_iterations, current_iteration=counter + 1),
                conversation_history=conversation_history,
                model='claude-3-7-sonnet-latest',
                max_tokens=budget_tokens * 10,
                thinking={
                    'type': 'enabled',
                    'budget_tokens': budget_tokens
                },
                tools=[simple_web_search_tool]
            ) 

            stop_reason_delta, conversation_history_delta = self.consume_stream(completion_res)
            print('current stop reason', stop_reason_delta, 'counter', counter)
            stop_reason = stop_reason_delta
            conversation_history.extend(conversation_history_delta)
            counter += 1
        deep_search_result = "\n###\n".join([ chat_message.model_dump_json(indent=2) for chat_message in conversation_history_delta ])
        # summaryze the conversation history
        return [
            {
                'type': 'text',
                'text': deep_search_result
            }
        ]
    
    def handle_tool(self, tool_name:str, tool_args:str, tool_use_id:str) -> ChatMessage:
        try:
            tool_function = attrgetter(tool_name)(self)
            arguments = json.loads(tool_args)
            tool_result_content:List[Dict] = tool_function(**arguments)
            return ChatMessage(
                role=Role.USER, 
                content=[
                    {
                        'type': 'tool_result',
                        'tool_use_id': tool_use_id,
                        'content': tool_result_content
                    }
                ]
            )
        except Exception as e:
            logger.error(f'error: {e}')
            return ChatMessage(
                role=Role.USER,
                content=[
                    {
                        'type': 'tool_result',
                        'tool_use_id': tool_use_id,
                        'is_error': True,
                        'content': str(e)
                    }
                ]
            )

    def consume_stream(self, stream:Iterable[RawMessageStreamEvent]) -> Tuple[StopReason, List[ChatMessage]]:
        conversation_history:List[ChatMessage] = []
        stop_reason = StopReason.END_TURN
        content:List[Dict] = []
        current_block_type = None
        text, signature, thinking, tool_name, tool_args, tool_use_id = None, None, None, None, None, None
        for event in stream:
            match event.type:
                case 'message_start':
                    print('')
                case 'message_delta':
                    stop_reason = event.delta.stop_reason
                    conversation_history.append(ChatMessage(role=Role.ASSISTANT, content=content))
                    if stop_reason != StopReason.TOOL_USE:
                        continue
                    print(tool_name)
                    print(tool_args)
                    tool_result = self.handle_tool(tool_name, tool_args, tool_use_id)
                    conversation_history.append(tool_result)
                case 'content_block_start':
                    current_block_type = event.content_block.type
                    match event.content_block.type:
                        case 'text': 
                            print('<response>')
                            text = event.content_block.text
                        case 'thinking': 
                            print('<thinking>')
                            thinking = event.content_block.thinking
                            signature = event.content_block.signature
                        case 'tool_use':
                            print('<tool_use>')
                            tool_name = event.content_block.name
                            tool_args = ''
                            tool_use_id = event.content_block.id
                case 'content_block_delta':
                    match event.delta.type:
                        case 'text_delta':
                            print(event.delta.text, end='', flush=True)
                            text = text + event.delta.text 
                        case 'thinking_delta':
                            print(event.delta.thinking, end='', flush=True)
                            thinking = thinking + event.delta.thinking
                        case 'signature_delta':
                            signature = signature + event.delta.signature
                        case 'input_json_delta':
                            tool_args = tool_args + event.delta.partial_json 
                case 'content_block_stop':
                    print('')
                    match current_block_type:
                        case 'text':
                            print('</response>')
                            content.append({'type': 'text', 'text': text})  
                        case 'thinking':
                            print('</thinking>')
                            content.append({'type': 'thinking', 'thinking': thinking, 'signature': signature})
                        case 'tool_use':
                            print('</tool_use>')
                            content.append({'type': 'tool_use', 'name': tool_name, 'input': json.loads(tool_args), 'id': tool_use_id})
            # end match event.type 
        # end for event in stream
        return stop_reason, conversation_history
    
    def handle_conversation(self, conversation_history:List[ChatMessage], system:str, model:str='claude-3-5-sonnet-latest', max_tokens:int=2048, thinking={'type': 'disabled'}, tools=[]) -> Optional[Iterable[RawMessageStreamEvent]]:
        try:
            anthropic_client = Anthropic(api_key=self.anthropic_api_key)
            completion_res:Iterable[RawMessageStreamEvent] = anthropic_client.messages.create(
                model=model, 
                messages=conversation_history,
                system=system,
                max_tokens=max_tokens,
                stream=True,
                thinking=thinking, 
                tools=tools
            )
            return completion_res
        except Exception as e:
            logger.error(f'error: {e}')
            
    def run(self) -> None:
        stop_reason = StopReason.END_TURN
        conversation_history:List[ChatMessage] = []
        while True:
            try:
                if stop_reason != StopReason.TOOL_USE:
                    query = input('query: ')
                    user_message = ChatMessage(role=Role.USER, content=query)
                    conversation_history.append(user_message)
                
                completion_res = self.handle_conversation(conversation_history, SystemPromptDefinitions.MAIN_AGENT_LOOP, tools=[deep_iterattive_web_search_tool])
                if completion_res is None:
                    logger.error('error: completion_res is None')
                    continue
                
                stop_reason_delta, conversation_history_delta = self.consume_stream(completion_res)
                stop_reason = stop_reason_delta
                conversation_history.extend(conversation_history_delta)
            except KeyboardInterrupt:
                logger.info('exiting...')
                break
            except Exception as e:
                logger.error(f'error: {e}')
                break  

