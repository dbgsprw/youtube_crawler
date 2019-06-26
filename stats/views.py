from rest_framework import viewsets, mixins

from stats import serializers, models


class VideoViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = serializers.VideoSerializer
    queryset = models.Video.objects.filter().all().order_by('-published_at')
