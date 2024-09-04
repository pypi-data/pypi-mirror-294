from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.parallels.views import (
    ParallelsViewSet,
)


router = SimpleRouter()

router.register('parallels', ParallelsViewSet, basename='parallels')
