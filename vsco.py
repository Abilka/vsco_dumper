import json
import os
import threading
import requests
from bs4 import BeautifulSoup
import head

class VSCO:
    def __init__(self, account_name: str):
        self.account_name = account_name


    def download_picture(self) -> bool:
        headers = head.headers[0]
        headers['referer'] = headers['referer'].format(self.account_name)

        '''parse main gallery photos and take all params'''
        response = requests.get(f'https://vsco.co/{self.account_name}/gallery', headers=headers)


        """take json data with in button 'load more'"""
        soup = BeautifulSoup(response.content, 'html5lib')
        profile_data = soup.find_all('script')[5].text.replace('window.__PRELOADED_STATE__ = ', '')
        profile_data = json.loads(profile_data)
        profile_images = profile_data['entities']['images']

        user_picture_packet = []

        user_picture_packet.append(list(map(lambda x: 'https://' + profile_images[x]['responsiveUrl'], profile_images)))

        try:
            self.site_id = profile_data['sites']['siteByUsername'][self.account_name]['site']['id']
        except:
            return False
        self.auth_token = profile_data['users']['currentUser']['tkn']
        self.account_id = profile_data['sites']['siteByUsername'][self.account_name]['site']['userId']

        params = (
            ('site_id', self.site_id),
            ('limit', '14'),
            ('cursor', profile_data['medias']['bySiteId'][str(self.site_id)]['nextCursor']),
        )

        headers = head.headers[1]
        headers['authorization'] = headers['authorization'].format(self.auth_token)


        """parse other photos with click load more"""
        response = requests.get('https://vsco.co/api/3.0/medias/profile', headers=headers, params=params)
        profile_data = response.json()
        user_picture_packet.append(list(
            map(lambda x: 'https://' + x['image']['responsive_url'] if x['type'] == 'image' else None,
                profile_data['media'])))

        while profile_data.get('next_cursor') is not None:
            params = (
                ('site_id', self.site_id),
                ('limit', '14'),
                ('cursor', profile_data['next_cursor']),
            )
            response = requests.get('https://vsco.co/api/3.0/medias/profile', headers=headers, params=params)
            profile_data = response.json()
            user_picture_packet.append(list(
                map(lambda x: 'https://' + x['image']['responsive_url'] if x['type'] == 'image' else None,
                    profile_data['media'])))

        if self.account_name not in os.listdir():
            os.mkdir(self.account_name)

        for pic_packet in user_picture_packet:
            for pic in pic_packet:
                if pic is not None:
                    threading.Thread(target=self.load_with_url, args=(pic,)).start()
        return True

    def load_with_url(self, url: str) -> bool:
        """
            :param url:  url-address download picture
            :return bool
        """
        headers = head.headers[0]

        path = self.account_name
        filename = self.account_name + '_' + url.split('/')[-1]
        with open(path + '/' + filename, 'wb') as f:
            response = requests.get(url, headers=headers, stream=True)
            if response.status_code == 200:
                f.write(response.content)
            else:
                split_server_adr = url.split('/', 4)
                url_download = f'https://image-{split_server_adr[3]}.vsco.co/{split_server_adr[4]}'
                f.write(requests.get(url_download, stream=True, headers=headers).content)
        return True

