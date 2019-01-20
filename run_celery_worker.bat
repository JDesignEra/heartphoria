@echo off
celery -A heartphoria.task.celery worker -P gevent