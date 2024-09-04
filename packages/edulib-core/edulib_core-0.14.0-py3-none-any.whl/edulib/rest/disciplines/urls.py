from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.disciplines.views import (
    DisciplineViewSet,
)


router = SimpleRouter()

router.register('disciplines', DisciplineViewSet, basename='disciplines')
