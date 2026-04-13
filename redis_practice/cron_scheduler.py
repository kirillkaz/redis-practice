from rq import cron

from redis_practice.entities.typehints import QueuesEnum
from redis_practice.tasks.gen_tasks import gen_orders_task
from redis_practice.tasks.clear_cache import clear_cache_task

cron.register(
    gen_orders_task,
    queue_name=QueuesEnum.GEN_QUEUE.value,
    interval=5,
)

cron.register(
    clear_cache_task,
    queue_name=QueuesEnum.CLEAR_QUEUE.value,
    interval=60,
)
