import logging 
from os import getenv 
from sys import stdout, stderr 

log_level = getenv('LOG_LEVEL', 'INFO')
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)03d - %(message)s'
logging.basicConfig(
    level=log_level,
    format=log_format,
    handlers=[
        logging.StreamHandler(stdout),
        logging.FileHandler('anthropic_openai.log')
    ]
)

logger = logging.getLogger('anthropic_openai')
for handler in logger.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.flush = True 


if __name__ == '__main__':
    logger.info('log was initialized')