import datetime

from django.db import models


class Video(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    channel_id = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    published_at = models.DateTimeField(null=True)
    thumbnail = models.URLField(null=True)


class Stats(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    view_count = models.IntegerField(null=True)
    like_count = models.IntegerField(null=True)
    dislike_count = models.IntegerField(null=True)
    favorite_count = models.IntegerField(null=True)
    comment_count = models.IntegerField(null=True)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0)
        return super(Stats, self).save(*args, **kwargs)
