import datetime

from django.db import models


class Video(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    channel_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    published_at = models.DateTimeField()


class Stats(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    view_count = models.IntegerField(blank=True, null=True)
    like_count = models.IntegerField(blank=True, null=True)
    dislike_count = models.IntegerField(blank=True, null=True)
    favorite_count = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0)
        return super(Stats, self).save(*args, **kwargs)
