import requests
from loguru import logger

r = requests.get('http://localhost:8000/print/1/2')
logger.info(f'first status code: {r.status_code}')
logger.info(f'first status code: {r.text}')

r = requests.post(
    'http://localhost:8000/user/validate',
    json={'name': 'zaza', 'surname': 'zaza', 'age': 20}
)
logger.info(f'second status code: {r.status_code}')
logger.info(f'second text: {r.json()}')
