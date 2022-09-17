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

headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11' }


class Assets(object):

    BASE_URL = 'https://api.opensea.io/api'

    def __init__(self, ):
        pass

    def get_owner_assets(self, owner, limit=50, cursor=''):
        proxies = get_proxies()
        assets_lst = []
 
        data = scraper.get(f"{Assets.BASE_URL}/v1/assets?owner={owner}&order_direction=asc&limit={limit}&cursor={cursor}&format=json", 
            headers=headers, timeout=10).json()

        next_ = data.get('next')
        assets = data.get('assets')
        detail = data.get('detail')

        if detail:
            raise Exception(f'request error: {detail}')

        full_assets = []
        for asset in assets:
            asset_id = f'{asset["asset_contract"]["address"]}-{asset["token_id"]}'
            asset['asset_id'] = asset_id
            full_assets.append(asset)
        return {
            'assets': full_assets,
            'cursor': next_
        }
    
    def get_single_asset(self, contract, idx):
        proxies = get_proxies()
        try:
            data = scraper.get(f"{Assets.BASE_URL}/v1/asset/{contract}/{idx}?format=json", headers=headers, 
                timeout=10).json()
        except Exception as err:
            msg = f'contract_addr [{contract}] idx [{idx}] error: {err}'
            print(msg)
            return None
        return data

  
assets = Assets()


if __name__ == '__main__':
    print(assets.get_owner_assets('0xc892Eb27936E867a25F1bd7585156f69EA34adAE'))
    #print(assets.get_single_asset('0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb', '1'))

