import datetime
import secrets
from urllib import parse

import requests
from dateutil.relativedelta import relativedelta


class YoutubeAPI:
    class YoutubeAPIException(Exception):
        pass

    YOUTUBE_API_URI = 'https://www.googleapis.com/youtube/v3'

    def __init__(self, channel_id, key_list):
        self.channel_id = channel_id
        self.key_list = key_list

    def get_full_uri(self, api, parameters):
        parameters.update(key=secrets.choice(self.key_list))
        query_strings = parse.urlencode(parameters)
        return f'{self.YOUTUBE_API_URI}/{api}?{query_strings}'

    def get(self, api, parameters):
        uri = self.get_full_uri(api=api, parameters=parameters)
        response = requests.get(uri)

        if response.status_code == 200:
            return requests.get(uri).json()
        else:
            raise self.YoutubeAPIException(response.json())

    def get_popular_videos(self):
        return self.get(api='videos',
                        parameters={
                            'regionCode': 'kr',
                            'chart': 'mostPopular',
                            'part': 'snippet, contentDetails, statistics, status'
                        })

    def get_videos_by_id_list(self, video_id_list):
        response = self.get(api='videos',
                            parameters={
                                'id': ','.join(video_id_list),
                                'part': 'snippet, statistics'
                            })

        for item in response['items']:
            yield item

    def get_videos_with_pagination(self, parameters):
        while True:
            response = self.get(api='search', parameters=parameters)
            items = response['items']

            for item in items:
                yield item

            if 'nextPageToken' not in response or not response['items']:
                return
            next_page_token = response['nextPageToken']
            parameters.update({'pageToken': next_page_token})

    # 단순히 page token을 통해 전부 가져올 시 동영상이 누락되는 현상이 있어, 1달 간격으로 나눠서 수집
    def get_all_videos(self):
        published_before = datetime.datetime.now()
        first_day = datetime.datetime(year=published_before.year, month=published_before.month, day=1)
        published_after = first_day - relativedelta(microseconds=1)

        while published_before > datetime.datetime(2013, 12, 31, 23, 59, 59, 999999):
            parameters = {
                'part': 'id',
                'type': 'video',
                'channelId': self.channel_id,
                'maxResults': 50,
                'order': 'date',
                'publishedAfter': published_after.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'publishedBefore': published_before.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            }

            yield from self.get_videos_with_pagination(parameters)

            published_before = published_after
            published_after = published_after - relativedelta(months=1)
