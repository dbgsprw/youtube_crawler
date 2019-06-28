import datetime
from urllib import parse

import requests


class YoutubeAPI:
    class YoutubeAPIException(Exception):
        pass

    YOUTUBE_API_URI = 'https://www.googleapis.com/youtube/v3'

    def get_popular_videos(self):
        return self.get(api='videos',
                        parameters={
                            'regionCode': 'kr',
                            'chart': 'mostPopular',
                            'part': 'snippet, contentDetails, statistics, status'
                        })

    def get_videos_by_id_list(self, video_id_list, part):
        response = self.get(api='videos',
                            parameters={
                                'id': ','.join(video_id_list),
                                'part': part
                            })

        for item in response['items']:
            yield item

    def get_videos_after(self, latest_video):
        parameters = {
            'part': 'id, snippet',
            'type': 'video',
            'channelId': self.channel_id,
            'maxResults': 50,
            'order': 'date',
        }

        if latest_video:
            parameters.update({
                'publishedAfter': (latest_video.published_at +
                                   datetime.timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            })

        yield from self.get_videos_with_pagination(parameters)

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

    def __init__(self, channel_id, key):
        self.channel_id = channel_id
        self.key = key

    def get(self, api, parameters):
        uri = self.get_full_uri(api=api, parameters=parameters)
        response = requests.get(uri)

        if response.status_code == 200:
            return requests.get(uri).json()
        else:
            raise self.YoutubeAPIException(response.json())

    def get_full_uri(self, api, parameters):
        parameters.update(key=self.key)
        query_strings = parse.urlencode(parameters)
        return f'{self.YOUTUBE_API_URI}/{api}?{query_strings}'
