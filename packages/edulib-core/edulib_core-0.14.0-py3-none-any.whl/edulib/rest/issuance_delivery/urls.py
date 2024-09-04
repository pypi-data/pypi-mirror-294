from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.issuance_delivery.views import (
    IssuanceDeliveryViewSet,
)


router = SimpleRouter()

router.register('issuances', IssuanceDeliveryViewSet, basename='issuances')
