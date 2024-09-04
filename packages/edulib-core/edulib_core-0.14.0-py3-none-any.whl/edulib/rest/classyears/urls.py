from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.classyears.views import (
    ClassYearViewSet,
)


router = SimpleRouter()

router.register('class_years', ClassYearViewSet, basename='classyears')
