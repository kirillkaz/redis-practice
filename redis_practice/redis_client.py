from redis import Redis as Redis
from redis_practice.config import config

redis_client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
