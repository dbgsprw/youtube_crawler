import datetime
import itertools

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand

from stats.management.commands import _youtube
from stats.models import Video, Stats


class Command(BaseCommand):
    help = 'Update Videos Info'

    def add_arguments(self, parser):
        parser.add_argument('channel_id', help='youtube channel id')
        parser.add_argument('key', help='Google api key')

    def handle(self, *args, **options):
        self.youtube_api = _youtube.YoutubeAPI(channel_id=options['channel_id'],
                                               key=options['key'])

        self.update_video_stats_from(self.get_new_video_ids_from_api())

    def get_new_video_ids_from_api(self):
        videos = self.youtube_api.get_all_videos(self.get_continued_time())

        for video in videos:
            video_id = video['id']['videoId']

            yield video_id

    def get_continued_time(self):
        try:
            latest_stat = self.get_latest_stat()
            if latest_stat.video != self.get_first_video():
                return latest_stat.video.published_at - relativedelta(microseconds=1)

        except Exception as e:
            pass

        return datetime.datetime.utcnow()

    def get_first_video(self):
        return Video.objects.filter().order_by('published_at')[0]

    def get_latest_stat(self):
        return Stats.objects.filter().order_by('-created_at', '-id')[0]

    def update_video_stats_from(self, generator):
        while True:
            id_list = list(itertools.islice(generator, 50))

            if not id_list:
                break

            self.update_video_and_stats(id_list)

    def update_video_and_stats(self, video_id_list):
        for video_detail in self.youtube_api.get_videos_by_id_list(video_id_list):
            published_at = datetime.datetime.strptime(video_detail['snippet']['publishedAt'],
                                                      '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=datetime.timezone.utc)

            Video.objects.update_or_create(id=video_detail['id'],
                                           defaults={
                                               "channel_id": video_detail['snippet']['channelId'],
                                               "title": video_detail['snippet']['title'],
                                               "description": video_detail['snippet']['description'],
                                               "published_at": published_at
                                           })
            self.save_stat(video_detail)

    def save_stat(self, video_detail):
        stats = video_detail['statistics']

        Stats(video_id=video_detail['id'],
              view_count=stats.get('viewCount', None),
              like_count=stats.get('likeCount', None),
              dislike_count=stats.get('dislikeCount', None),
              favorite_count=stats.get('favoriteCount', None),
              comment_count=stats.get('commentCount', None)).save()
