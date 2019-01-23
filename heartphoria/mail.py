from socket import socket, AF_INET, SOCK_STREAM

import yagmail


def __init_mail():
    return yagmail.SMTP({'jdesignera.dev@gmail.com': 'Heartphoria'}, oauth2_file='oauth2_creds.json')


def mail(to, subject, contents):
    try:
        yag = __init_mail()
        yag.send(
            to=to,
            subject=subject,
            contents=str(contents).replace('\n', '')
        )
    except TimeoutError:
        print('Gmail port  587 is blocked. Email will not be send...')


def send_mail(to, subject, contents):
    from heartphoria.task import celery_send_mail, check_celery_worker_status

    if check_celery_worker_status():
        print('Sending Mail Synchronously...')
        mail(to, subject, contents)
    else:
        print('Sending Mail In Background...')
        celery_send_mail.delay(to, subject, contents)
