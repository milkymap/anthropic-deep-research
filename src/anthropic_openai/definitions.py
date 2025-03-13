from typing import List, Tuple, Dict 
from enum import Enum 

class SystemPromptDefinitions(str, Enum):
    MAIN_AGENT_LOOP:str = '''
    You are a helpful assistant with access to an advanced deep iterative web search capability.

    DEEP WEB RESEARCH CAPABILITIES:
    - When information gathering is required, utilize the 'deep_iterative_web_search' tool
    - This tool performs comprehensive, multi-level research through successive search refinements
    - The search process explores topics with increasing depth, identifies key subtopics, resolves knowledge gaps, and cross-references information across credible sources
    - Information is verified across multiple reliable sources and presented with clear citations
    - The tool adapts its search strategy based on complexity level, with higher complexity triggering more extensive iterations and deeper analysis

    HOW TO USE THE SEARCH TOOL:
    - Invoke this tool by formulating:
    * query: A clear, concise reformulation of the original question
    * task_complexity: Set as 'low', 'medium', or 'high' based on research depth required
    - Low complexity: Quick factual lookups, definitions, straightforward information
    - Medium complexity: Topics requiring multiple perspectives, historical context, or moderate technical understanding
    - High complexity: In-depth research questions, specialized domains, emerging topics with limited information, or subjects with conflicting viewpoints

    WORKFLOW APPROACH:
    - Break complex queries into logical sub-questions when appropriate
    - Analyze and synthesize search results to provide comprehensive answers
    - Clearly distinguish between factual information and interpretations/opinions
    - Present information in a structured, easy-to-understand format
    - Acknowledge limitations when definitive information isn't available

    Respond to queries in a clear, helpful manner, leveraging your deep web research capabilities to provide thorough, accurate, and well-sourced information.
    Be kind, patient, and attentive to the user's needs, ensuring a positive and informative interaction.
    '''
    DEEP_ITERATIVE_WEB_SEARCH:str = ('''
    TASK: Conduct a deep iterative web search to provide comprehensive, accurate, and up-to-date information.
    MAX ITERATIONS: {max_iterations}
    CURRENT ITERATION: {current_iteration}
                                     
    SEARCH METHODOLOGY:
    1. Begin with broad search queries to establish baseline understanding
    2. Identify key subtopics, perspectives, and knowledge gaps from initial results
    3. Formulate increasingly specific search queries based on each iteration
    4. Cross-reference information across multiple credible sources
    5. Prioritize recent sources when searching time-sensitive topics
    6. Track search history to avoid circular searching

    ITERATION PROCESS:
    - After each search result, analyze:
    * What new information was discovered?
    * What questions remain unanswered?
    * What conflicting information requires verification?
    * What specialized terminology could improve future queries?
    - Document each search query used and summarize key findings
    - Include 3-5 new search queries to explore next based on current findings

    DELIVERABLE FORMAT:
    1. Executive Summary (key findings and conclusions)
    2. Detailed Analysis (organized by subtopic)
    3. Evidence Summary (with direct quotes and URLs from credible sources)
    4. Remaining Questions (areas where information is incomplete or conflicting)
    5. Search Process Documentation (queries used and evolution of search strategy)

    QUALITY CRITERIA:
    - Information from at least 7 distinct credible sources
    - Representation of multiple perspectives when topic is subjective
    - Clear distinction between factual information and interpretation
    - Citation of primary sources when available
    - Transparent acknowledgment of information limitations
    ''')

deep_iterattive_web_search_tool =  {
    'name': 'deep_iterative_web_search',
    'description': 'Performs comprehensive, multi-level web research through iterative search refinement. This tool conducts successive search queries that build upon previous results, exploring a topic with increasing depth and specificity. The process includes identifying key subtopics, resolving knowledge gaps, cross-referencing information across credible sources, and documenting the search evolution. Particularly valuable for complex research questions requiring thorough investigation beyond surface-level information. The tool adapts its search strategy based on task complexity, with higher complexity levels triggering more extensive iterations, specialized terminology exploration, and deeper analysis of conflicting information. Returns structured findings with source citations, multiple perspectives, and clearly distinguished factual versus interpretive content.',
    'input_schema':{
        'type': 'object',
        'properties': {
            'query': {
                'type': 'string', 
                'description': 'A clear and concise reformulation of the original user query to search for.'
            },
            'user_contraints':{
                'type': 'string',
                'description': 'A detailed summary of what the user realy want.'
            },
            'task_complexity': {
                'type': 'string',
                'enum': ['low', 'medium', 'high'], 
                'description': 'The complexity of the task, which can be one of "low", "medium", or "high".'
            },
            'max_iterations': {
                'type': 'integer',
                'description': 'The maximum number of iterations to be performed during the search. do not exceed 10 iterations. task_complextity=low, max_iterations=3; task_complextity=medium, max_iterations=5; task_complextity=high, max_iterations=10.'
            }
        }, 
        'required': ['query', 'task_complexity', 'max_iterations'],
    }
}

simple_web_search_tool = {
    'name': 'simple_web_search',
    'description': 'Performs parallel web searches with intelligent aggregation of results. This tool accepts multiple search queries simultaneously, conducts independent searches for each, and synthesizes findings into a cohesive response. Unlike basic search tools, it employs an LLM to process and reformulate raw search results, extracting key information, removing redundancies, and presenting findings in a clear, organized format. The tool excels at breaking complex questions into component parts that can be researched separately and then reassembled. Each expanded query can target specific aspects, perspectives, or timeframes related to the main question. Results include information from diverse, credible sources with appropriate attributions. Ideal for questions requiring breadth rather than depth, or for initial research that may lead to more focused deep iterative searching.',
    'input_schema': {
        'type': 'object',
        'properties': {
            'expanded_queries': {
                'type': 'array',
                'items': {
                    'type': 'string', 
                    'description': 'The expanded search query(as a question) to be looked up on the web for a specific sub topic.'
                },
                'description': 'A list of expanded search queries to be looked up on the web for specific subtopics.'
            }, 
            'search_context_size': {
                'type': 'string',
                'enum': ['low', 'medium', 'high'],
                'description': 'The size of the search context to be used for the search.'
            }
        }, 
        'required': ['expanded_queries', 'search_context_size']
    }
}