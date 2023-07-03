from rest_framework import routers

from .views import WineViewSet

router = routers.DefaultRouter()

router.register("wine", WineViewSet, "wines")

urlpatterns = router.urls
print(urlpatterns)
