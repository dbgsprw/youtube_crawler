from rest_framework.routers import DefaultRouter

from stats.views import VideoViewSet

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='videos')
urlpatterns = router.urls
