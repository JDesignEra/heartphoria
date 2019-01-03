import yagmail


def init_mail():
    return yagmail.SMTP({'jdesignera.dev@gmail.com': 'Heartphoria'}, oauth2_file='oauth2_creds.json')


def send_mail(to, subject, contents):
    yag = init_mail()
    yag.send(
        to=to,
        subject=subject,
        contents=contents
    )
