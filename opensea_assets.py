import cloudscraper

from proxy_generator import get_proxies


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


class Assets(object):

    BASE_URL = 'https://api.opensea.io/api'

    def __init__(self, ):
        pass

    def get_owner_assets(self, owner):
        proxies = get_proxies()
        assets_lst = []
        cursor = ''
        while True:
            data = scraper.get(f"{Assets.BASE_URL}/v1/assets?owner={owner}&order_direction=asc&limit=50&cursor={cursor}&format=json", 
                headers=headers, proxies=proxies, timeout=1.5).json()
            next_ = data.get('next')
            assets = data.get('assets')
            detail = data.get('detail')

            if detail:
                raise Exception(f'request error: {detail}')
            if assets:
                assets_lst.append(assets)    
            if next_:
                cursor = next_
                continue
            else:
                break

        full_assets = []
        for data in assets_lst:
            for asset in data:
                new_id = f'{asset["asset_contract"]["address"]}-{asset["token_id"]}'
                asset['new_id'] = new_id
                full_assets.append(asset)
        return full_assets
    
    def get_single_asset(self, contract, idx):
        proxies = get_proxies()
        try:
            data = scraper.get(f"{Assets.BASE_URL}/v1/asset/{contract}/{idx}?format=json", headers=headers, 
                proxies=proxies, timeout=1.5).json()
        except Exception as err:
            logging.info(f'contract_addr [{contract}] idx [{idx}] error: {err}')
            return None
        return data

  
assets = Assets()


if __name__ == '__main__':
    # print(assets.get_owner_assets('0xc892Eb27936E867a25F1bd7585156f69EA34adAE'))
    print(assets.get_single_asset('0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb', '1'))

