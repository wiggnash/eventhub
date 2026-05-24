from rest_framework import routers

from .views import EventViewSet

router = routers.SimpleRouter()
router.register(r'events', EventViewSet)

urlpatterns = router.urls
