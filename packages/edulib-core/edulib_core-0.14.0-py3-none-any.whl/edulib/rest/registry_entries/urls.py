from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.registry_entries.views import (
    EntryViewSet,
    GeneralFundViewSet,
)


router = SimpleRouter()

router.register('books_registry', EntryViewSet, basename='registry-entries')
router.register('general_fund', GeneralFundViewSet, basename='general-fund')
