from rq import cron

from redis_practice.entities.typehints import QueuesEnum
from redis_practice.tasks.gen_tasks import gen_orders_task

cron.register(
    gen_orders_task,
    queue_name=QueuesEnum.GEN_QUEUE.value,
    interval=5,
)
