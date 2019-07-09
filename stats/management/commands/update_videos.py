import datetime

from django.core.management.base import BaseCommand

from stats.management.commands import _youtube
from stats import helpers
from stats.models import Video


class Command(BaseCommand):
    help = 'Update video info'

    def add_arguments(self, parser):
        parser.add_argument('channel_id', help='youtube channel id')
        parser.add_argument('key', help='Google api key')
        parser.add_argument('--existing', action='store_const', const=True, default=False, help='update existing')

    def handle(self, *args, **options):
        self.youtube_api = _youtube.YoutubeAPI(channel_id=options['channel_id'],
                                               key=options['key'])

        if options['existing']:
            self.update_existing_videos()

        else:
            self.create_new_videos()

    def update_existing_videos(self):
        for video_id_list in helpers.get_sliced_list(Video.objects.order_by('-published_at').all().iterator()):
            for video_detail in self.youtube_api.get_videos_by_id_list(video_id_list, part='snippet'):
                self.create_or_update_video(video_detail)

    def create_new_videos(self):
        latest_video = self.get_latest_video()
        for video_detail in self.youtube_api.get_videos_after(latest_video):
            self.create_or_update_video(video_detail)

    def get_latest_video(self):
        return (Video.objects.filter().order_by('-published_at') or [None])[0]

    def create_or_update_video(self, video_detail):
        published_at = datetime.datetime.strptime(video_detail['snippet']['publishedAt'],
                                                  '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=datetime.timezone.utc)

        Video.objects.update_or_create(id=helpers.get_video_id(video_detail),
                                       defaults={
                                           "channel_id": video_detail['snippet']['channelId'],
                                           "title": video_detail['snippet']['title'],
                                           "description": video_detail['snippet']['description'],
                                           "published_at": published_at,
                                           "thumbnail": video_detail['snippet']['thumbnails']['high']['url']
                                       })
