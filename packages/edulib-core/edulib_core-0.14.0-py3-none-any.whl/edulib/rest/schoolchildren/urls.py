from rest_framework.routers import (
    SimpleRouter,
)

from .views import (
    SchoolchildViewSet,
)


router = SimpleRouter()
router.register(r'schoolchildren', SchoolchildViewSet, basename='schoolchildren')
