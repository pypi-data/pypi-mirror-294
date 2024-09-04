from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.academic_years.views import (
    AcademicYearViewSet,
)


router = SimpleRouter()

router.register('academic_years', AcademicYearViewSet, basename='academic-years')
