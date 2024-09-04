from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.udc import (
    views,
)


router = SimpleRouter()

router.register('udc', views.UdcViewSet, basename='udc')
