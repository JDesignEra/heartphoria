from heartphoria import app
from heartphoria.mail import mail
from celery import Celery
from kombu import exceptions, Connection


def make_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['result_backend'],
                    broker=app.config['broker_url'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)


def get_celery_worker_status():
    error = "error"
    result = {}

    try:
        conn = Connection(app.config['broker_url'])
        conn.ensure_connection(max_retries=1)

    except exceptions.OperationalError as e:
        result = {error: str(e)}

    if 'error' not in result:
        workers = celery.control.inspect().active()

        if not workers:
            result = {error: 'No active workers.'}

    return result


@celery.task()
def celery_send_mail(to, subject, content):
    with app.app_context():
        mail(to, subject, content)
