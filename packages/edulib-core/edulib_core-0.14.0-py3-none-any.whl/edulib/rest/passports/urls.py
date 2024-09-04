from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.passports.views import (
    CleanupDayViewSet,
    DocumentViewSet,
    PassportViewSet,
    WorkModeViewSet,
)


router = SimpleRouter()

router.register('libraries', PassportViewSet, basename='libraries')


router.register(
    r'libraries/(?P<lib_passport_id>\d+)/work_modes',
    WorkModeViewSet,
    basename='work-modes'
)
router.register(
    r'libraries/(?P<lib_passport_id>\d+)/documents',
    DocumentViewSet,
    basename='documents'
)
router.register(
    r'libraries/(?P<lib_passport_id>\d+)/cleanup_days',
    CleanupDayViewSet,
    basename='cleanup-days'
)
