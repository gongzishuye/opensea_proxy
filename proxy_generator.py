import random
import requests

from decouple import config
from flask_apscheduler import APScheduler


scheduler = APScheduler()
TOKEN = config('TOKEN')
IP_NUM = config('IP_NUM')
print(f'Token: {TOKEN}, IP number: {IP_NUM}')
URL = f'http://list.rola.info:8088/user_get_ip_list?token={TOKEN}&qty={IP_NUM}' + \
    '&country=us&state=&city=&time=10&format=json&protocol=http&filter=1&area=us'
proxies = []


def get_proxies():
    global proxies
    domain = '' if not proxies else random.choice(proxies)
    domain = '' if not domain else domain
    print(f'Using domain: {domain}')
    return {
        'https': domain
    }


@scheduler.task('interval', id='proxy', seconds=60 * 5)
def generate_proxies():
    print('Refreshing proxies...')
    resp = requests.get(URL).json()
    domains = resp['data']
    print(resp)
    global proxies
    proxies = domains
    proxies.append(None)
    print(proxies)


generate_proxies()
