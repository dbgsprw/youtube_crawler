from stats.models import Stats


def calculate_view_diff(video, start_day, end_day):
    older_stat = video.stats_set.filter(created_at__gte=start_day).order_by('created_at')[0]
    newer_stat = video.stats_set.filter(created_at__lte=end_day).order_by('-created_at')[0]

    if newer_stat == older_stat:
        older_stat = Stats(view_count=0, created_at=video.published_at)

    total_seconds = (end_day - start_day).total_seconds()
    return _get_average_view_per_seconds(older_stat, newer_stat) * total_seconds


def _get_average_view_per_seconds(older_stat, newer_stat):
    return (newer_stat.view_count - older_stat.view_count) / \
           (newer_stat.created_at - older_stat.created_at).total_seconds()
