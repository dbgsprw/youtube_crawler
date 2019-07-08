from django.core.management.base import BaseCommand

from stats.models import Stats


def get_average_view_per_seconds(older_stat, newer_stat):
    return (newer_stat.view_count - older_stat.view_count) / \
           (newer_stat.created_at - older_stat.created_at).total_seconds()


def sort_by_view_count_in_range(start_day, end_day):
    def func(video):
        try:
            older_stat = video.stats_set.filter(created_at__gte=start_day).order_by('created_at')[0]
            newer_stat = video.stats_set.filter(created_at__lte=end_day).order_by('-created_at')[0]
        except IndexError as e:
            return 0

        if newer_stat == older_stat:
            older_stat = Stats(view_count=0, created_at=video.published_at)

        video.average_view = get_average_view_per_seconds(older_stat, newer_stat)
        return video.average_view

    return func


class Command(BaseCommand):
    help = 'Show div'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
