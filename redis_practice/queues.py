from rq import Queue

from redis_practice.redis_client import redis_client
from redis_practice.entities.typehints import QueuesEnum

gen_q = Queue(name=QueuesEnum.GEN_QUEUE.value, connection=redis_client)
api_q = Queue(name=QueuesEnum.API_QUEUE.value, connection=redis_client)
