import logging

import cloudscraper
from fake_useragent import UserAgent

from proxy_generator import get_proxies


ua = UserAgent()

# This creates a new Scraper instance that can get past the OpenSea Cloudflare protections
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }
)

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}


class Collection(object):

    BASE_URL = 'https://api.opensea.io/api'
    
    def __init__(self,):
        pass

    def get_contract(self, contract_addr):
        proxies = get_proxies()
        headers = { 'User-Agent': ua.random }
        try:
            data = scraper.get(f"{self.BASE_URL}/v1/asset_contract/{contract_addr}?format=json", 
                headers=headers, proxies=proxies, timeout=1.5).json()
        except Exception as err:
            print(f'contract_addr [{contract_addr}] error: {err}')
            return None
        if not data.get('collection'):
            print(f'contract_addr [{contract_addr}] receive bad data: {data}')
        return data

    def get_collection(self, slug):
        proxies = get_proxies()
        headers = { 'User-Agent': ua.random }
        try:
            data = scraper.get(f"{self.BASE_URL}/v1/collection/{slug}?format=json", 
                headers=headers, proxies=proxies, timeout=1.5).json()
        except Exception as err:
            print(f'slug [{slug}] error: {err}')
            return None
        return data
    
    def get_stats(self, slug):
        proxies = get_proxies()
        headers = { 'User-Agent': ua.random }
        try:
            data = scraper.get(f"{self.BASE_URL}/v1/collection/{slug}/stats?format=json", 
                headers=headers, proxies=proxies, timeout=1.5).json()
        except Exception as err:
            print(f'slug [{slug}] error: {err}')
            return None
        return data


collection = Collection()


if __name__ == '__main__':
    # print(collection.get_contract('0x06012c8cf97bead5deae237070f9587f8e7a266d'))
    # print(collection.get_collection('doodles-official'))
    print(collection.get_stats('doodles-official'))
