import yagmail


def init_mail():
    return yagmail.SMTP({'jdesignera.dev@gmail.com': 'Heartphoria'}, oauth2_file='oauth2_creds.json')


def mail(to, subject, contents):
    yag = init_mail()
    yag.send(
        to=to,
        subject=subject,
        contents=str(contents).replace('\n', '')
    )


def send_mail(to, subject, contents):
    from heartphoria.task import celery_send_mail, check_celery_worker_status

    if check_celery_worker_status():
        mail(to, subject, contents)
    else:
        celery_send_mail.delay(to, subject, contents)
