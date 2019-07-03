from collections import defaultdict

from django.core.management.base import BaseCommand

from stats.models import Stats


def get_average_view(older_stat, newer_stat):
    return (newer_stat.view_count - older_stat.view_count) / \
           (newer_stat.created_at - older_stat.created_at).total_seconds()


class Command(BaseCommand):
    help = 'Show div'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        stat_dict = defaultdict(list)

        for stat in Stats.objects.all().order_by("-created_at"):
            stat_dict[stat.video_id].append(stat)

        ll = [(stat_list[0].video_id, get_average_view(stat_list[1],
                                                       stat_list[0])) for key, stat_list in stat_dict.items()
              if len(stat_list) >= 2]

        ll = sorted(ll, key=lambda x: x[1], reverse=True)
