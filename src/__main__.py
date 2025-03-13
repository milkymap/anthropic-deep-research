import click 

from dotenv import load_dotenv

from anthropic_openai import AgentLoop, Role, ChatMessage, StopReason
from anthropic_openai.settings import Credentials

@click.group(chain=False, invoke_without_command=True)
@click.pass_context
def group_handler(ctx:click.core.Context):
    ctx.ensure_object(dict)
    ctx.obj['settings'] = {
        'credentials': Credentials()
    }


@group_handler.command()
@click.pass_context
def launch_engine(ctx:click.core.Context):
    settings = ctx.obj['settings']
    credentials:Credentials = settings['credentials']
    agent_loop = AgentLoop(openai_api_key=credentials.openai_api_key, anthropic_api_key=credentials.anthropic_api_key)
    agent_loop.run()

if __name__ == '__main__':
    load_dotenv()
    group_handler(obj={})

