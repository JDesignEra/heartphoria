from kombu import exceptions, Connection
from celery import Celery

from heartphoria import app
from heartphoria import db
from heartphoria.models import User
from heartphoria.mail import mail


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['result_backend'], broker=app.config['broker_url'])
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


def check_celery_worker_status():
    errors = {}

    try:
        conn = Connection(app.config['broker_url'])
        conn.ensure_connection(max_retries=1)

    except exceptions.OperationalError as e:
        errors = {'connection': str(e)}

    if not errors:
        workers = celery.control.inspect().active()

        if not workers:
            errors = {'workers': 'No active workers.'}

    return errors


@celery.on_after_configure.connect()
def periodic_tasks(sender, **kwargs):
    # Every 24 Hours
    sender.add_periodic_task(86400.0, remove_fcode, name='Reset Forgot Password Codes')


@celery.task()
def celery_send_mail(to, subject, content):
    with app.app_context():
        mail(to, subject, content)


@celery.task()
def remove_fcode():
    print('Removing All Forgot Password Codes...')
    users = User.query.filter(User.fcode is None or User.fcode != '').all()

    for user in users:
        user.fcode = None
        db.session.commit()