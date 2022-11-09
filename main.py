import os
import string

import time
import requests as rq


class Twitch:
    def __init__(self):
        self.token = str()
        self.client_id = os.environ['CLIENT_ID']
        self.favorite_streamer = ['streamer twitch url']

    def gettoken(self) -> string:
        """get app access token"""

        client_secret = os.environ['CLIENT_SECRET']

        gettoken = rq.post(
            'https://id.twitch.tv/oauth2/token',
            params={
                'client_id': self.client_id,
                'client_secret': client_secret,
                'grant_type': 'client_credentials'
            }
        )
        access_token = gettoken.json()
        self.token = f'Bearer {access_token["access_token"]}'

    def is_online_streamer(self):
        """Check if a streamer is online and get the streamer id"""

        if not self.token:
            self.gettoken()

        for streamer in self.favorite_streamer:
            name = self.get_streamer_name(streamer)
            getonlinestream = rq.get(f'{streamer}').content.decode('utf-8')
            if 'isLiveBroadcast' in getonlinestream:
                findstreamer = rq.get(
                    'https://api.twitch.tv/helix/users',
                    headers={
                        'Authorization': self.token,
                        'Client-Id': self.client_id
                    },
                    params={
                        'login': name,
                    }
                )

                if findstreamer.status_code != 200:

                    self.gettoken()
                else:
                    streamer = findstreamer.json()
                    streamer_id = streamer['data'][0]['id']
                    self.get_data_stream(streamer_id)
                    time.sleep(10)

    def get_data_stream(self, streamer_id: string) -> dict:
        """Get data of an online streamer"""

        data = rq.get(
            'https://api.twitch.tv/helix/streams',
            headers={
                'Authorization': self.token,
                'Client-Id': self.client_id
            },
            params={
                'user_id': streamer_id
            }
        )

        if data.status_code != 200:
            self.gettoken()
        return data.json()

    def get_streamer_name(self, url: string) -> string:
        """Get the name login of a streamer"""
        name = url.split('/')
        return name[-1]


if __name__ == "__main__":
    compt = 1
    while compt == 1:
        Twitch().is_online_streamer()
        time.sleep(60)
