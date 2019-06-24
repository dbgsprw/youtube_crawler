from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from stats.management.commands._youtube import YoutubeAPI


class YoutubeTestCase(TestCase):
    def setUp(self):
        self.youtube_api = YoutubeAPI(channel_id="channel_id",
                                      key_list=["key1"])

    def test_get_full_uri(self):
        actual = self.youtube_api.get_full_uri("foo", {'foo': 'bar'})
        expected = "https://www.googleapis.com/youtube/v3/foo?foo=bar&key=key1"

        self.assertEqual(actual, expected)

    @patch.object(YoutubeAPI, 'get_videos_with_pagination',
                  return_value=[None])
    def test_get_all_videos(self, mock_function):
        list(self.youtube_api.get_all_videos())

        mock_function.assert_called_with({
            'part': 'id',
            'type': 'video',
            'channelId': 'channel_id',
            'maxResults': 50,
            'order': 'date',
            'publishedAfter': '2013-12-28T23:59:59.999999Z',
            'publishedBefore': '2014-01-28T23:59:59.999999Z'})


class CommandsTestCase(TestCase):

    @patch.object(YoutubeAPI, 'get')
    def test_update(self, mock_get):
        args = ["channel_id", "key1", "key2"]
        opts = {}
        call_command('update', *args, **opts)
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
