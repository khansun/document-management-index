import yaml
from celery import Celery
from i3worker import config, utils
from celery.signals import setup_logging
from logging.config import dictConfig


settings = config.get_settings()

app = Celery(
    'i3worker',
    broker=settings.papermerge__redis__url,
    include=['i3worker.tasks']
)

app.conf.update(
    broker_connection_retry_on_startup=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    task_default_queue='i3',  # Set default queue
    task_routes={
        'index_add_node': {'queue': 'i3'},
        'i3worker.tasks.*': {'queue': 'i3'}
    }
)

app.autodiscover_tasks()

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
    max_retries=3,
    broker_connection_retry_on_startup=False,
    interval_start=0,
    interval_step=0.2,
    interval_max=0.2,
)


@setup_logging.connect
def config_loggers(*args, **kwags):
    if settings.papermerge__main__logging_cfg:
        utils.setup_logging(settings.papermerge__main__logging_cfg)


if __name__ == '__main__':
    app.start()
