from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.readers.views import (
    ReaderViewSet,
)


router = SimpleRouter()

router.register('readers', ReaderViewSet, basename='readers')
