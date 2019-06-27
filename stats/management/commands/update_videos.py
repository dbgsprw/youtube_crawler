import datetime

from django.core.management.base import BaseCommand

from stats.management.commands import _youtube
from stats.models import Video


class Command(BaseCommand):
    help = 'Update video info'

    def add_arguments(self, parser):
        parser.add_argument('channel_id', help='youtube channel id')
        parser.add_argument('key', help='Google api key')

    def handle(self, *args, **options):
        self.youtube_api = _youtube.YoutubeAPI(channel_id=options['channel_id'],
                                               key=options['key'])

        latest_video = self.get_latest_video()

        for video_detail in self.youtube_api.get_videos_after(latest_video):
            self.save_video(video_detail)

    def get_latest_video(self):
        return (Video.objects.filter().order_by('-published_at') or [None])[0]

    def save_video(self, video_detail):
        published_at = datetime.datetime.strptime(video_detail['snippet']['publishedAt'],
                                                  '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=datetime.timezone.utc)

        Video.objects.create(id=video_detail['id']['videoId'], channel_id=video_detail['snippet']['channelId'],
                             title=video_detail['snippet']['title'], description=video_detail['snippet']['description'],
                             published_at=published_at)
