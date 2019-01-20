@echo off
celery -A heartphoria.task.celery beat --loglevel=info