from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.schools.views import (
    SchoolViewSet,
)


router = SimpleRouter()

router.register('schools', SchoolViewSet, basename='schools')
