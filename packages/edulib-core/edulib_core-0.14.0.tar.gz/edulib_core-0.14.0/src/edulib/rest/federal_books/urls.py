from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.federal_books.views import (
    FederalBookViewSet,
)


router = SimpleRouter()

router.register('fed_books', FederalBookViewSet, basename='fed_books')
