import requests
import urllib3
import time

api='5055046495:AAHuvPRrZuCvxM7IHrGNrPDqROu8QZNvLl8'


def send_to_telegram(filepath, to_send):
    if to_send==1:
        chat_id='1001648926832'
    else:
        chat_id='1001328229950'
    file={"video":open(f'{filepath}', 'rb')}
    divider='●▬▬▬▬▬๑۩۩๑▬▬▬▬▬▬●'
    try:
        requests.get(f'https://api.telegram.org/bot{api}/sendMessage?chat_id=-{chat_id}&text={divider}')
        requests.post(f'https://api.telegram.org/bot{api}/sendVideo?chat_id=-{chat_id}', files=file)
    except (urllib3.exceptions.MaxRetryError, requests.exceptions.SSLError):
        time.sleep(5)
        requests.get(f'https://api.telegram.org/bot{api}/sendMessage?chat_id=-{chat_id}&text={divider}')
        requests.post(f'https://api.telegram.org/bot{api}/sendVideo?chat_id=-{chat_id}', files=file)
