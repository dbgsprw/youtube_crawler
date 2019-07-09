import datetime
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from stats import services
from stats.management.commands._youtube import YoutubeAPI
from stats.models import Stats, Video


class UpdateYoutubeTestCase(TestCase):
    def setUp(self):
        self.youtube_api = YoutubeAPI(channel_id="channel_id",
                                      key="key1")

    def test_get_full_uri(self):
        actual = self.youtube_api.get_full_uri("foo", {'foo': 'bar'})
        expected = "https://www.googleapis.com/youtube/v3/foo?foo=bar&key=key1"

        self.assertEqual(actual, expected)

    @patch.object(YoutubeAPI, 'get_videos_with_pagination',
                  return_value=[None])
    def test_get_videos_after(self, mock_function):
        now = datetime.datetime.now()
        list(self.youtube_api.get_videos_after(Video(published_at=now)))

        mock_function.assert_called_with({
            'part': 'id, snippet',
            'type': 'video',
            'channelId': 'channel_id',
            'maxResults': 50,
            'order': 'date',
            'publishedAfter': (now + datetime.timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')})


class CommandsTestCase(TestCase):

    @patch.object(YoutubeAPI, 'get')
    def test_update(self, mock_get):
        args = ["channel_id", "key1"]
        opts = {}
        call_command('update_videos', *args, **opts)
        mock_get.assert_called()

    def test_update_missing_arguments(self):
        with self.assertRaises(CommandError):
            args = []
            opts = {}
            call_command('update', *args, **opts)

        with self.assertRaises(CommandError):
            args = ["channel_id"]
            opts = {}
            call_command('update', *args, **opts)


class ServiceTestCase(TestCase):

    @patch.object(Video, 'stats_set',
                  return_value=[None])
    @patch.object(services, '_get_average_view_per_seconds',
                  return_value=100)
    def test_calculate_view_diff(self, mock_function, mock_set):
        test_video = Video()
        test_start_day = datetime.datetime(2015, 1, 1, 1, 1, 1)
        test_end_day = test_start_day + datetime.timedelta(days=1)
        total_seconds = (test_end_day - test_start_day).total_seconds()
        self.assertEqual(100 * total_seconds,
                         services.calculate_view_diff(test_video, test_start_day, test_end_day))

        mock_set.filter.assert_called()

    def test_get_average_view(self):
        older = Stats(created_at=datetime.datetime(2015, 1, 1, 1, 1, 1),
                      view_count=100)
        newer = Stats(created_at=datetime.datetime(2015, 1, 1, 1, 2, 40),
                      view_count=199)
        average_view = services._get_average_view_per_seconds(newer_stat=newer, older_stat=older)
        self.assertEqual(average_view, 1)
