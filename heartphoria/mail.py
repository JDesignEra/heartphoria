from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR

import yagmail


class Mail:
    def __init__(self):
        self.yag = yagmail.SMTP({'jdesignera.dev@gmail.com': 'Heartphoria'}, oauth2_file='oauth2_creds.json')

    def mail(self, to, subject, contents):
        if self.__check_port('smtp.gmail.com', 587):
            self.yag.send(
                to=to,
                subject=subject,
                contents=str(contents).replace('\n', '')
            )
        else:
            print('Gmail port 587 is probably blocked...')

    def send_mail(self, to, subject, contents):
        from heartphoria.task import celery_send_mail, check_celery_worker_status

        if check_celery_worker_status():
            print('Sending Mail Synchronously...')
            self.mail(to, subject, contents)
        else:
            print('Sending Mail In Background...')
            celery_send_mail.delay(to, subject, contents)

    def __check_port(self, ip, port):
        self.__s = socket(AF_INET, SOCK_STREAM)
        self.__s.settimeout(5)

        try:
            self.__s.connect((ip, int(port)))
            self.__s.shutdown(SHUT_RDWR)
            return True
        except:
            return False
        finally:
            self.__s.close()
