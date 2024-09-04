from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.examples.views import (
    RegistryExampleViewSet,
)


router = SimpleRouter()

router.register(r'books_registry/(?P<registryentry_id>\d+)/examples', RegistryExampleViewSet, basename='examples')
