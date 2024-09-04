from django.db.models import (
    OuterRef,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

from edulib.core.academic_years.models import (
    AcademicYear,
)
from edulib.core.classyears.models import (
    ClassYear,
)
from edulib.core.employees.models import (
    Employee,
)
from edulib.core.parallels.models import (
    Parallel,
)
from edulib.core.schools.models import (
    School,
)
from edulib.rest.classyears.filters import (
    ClassYearFilter,
)
from edulib.rest.classyears.serializers import (
    ClassYearSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class ClassYearViewSet(ReadOnlyModelViewSet):
    """Эндпоинты для работы с классами."""

    serializer_class = ClassYearSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = ClassYearFilter
    search_fields = ('name',)

    def get_queryset(self):
        school_query = School.objects.filter(id=OuterRef('school_id'))
        academic_year_query = AcademicYear.objects.filter(id=OuterRef('academic_year_id'))
        employee_query = Employee.objects.filter(id=OuterRef('teacher_id'))
        parallel_query = Parallel.objects.filter(id=OuterRef('parallel_id'))

        return ClassYear.objects.annotate(
            school__short_name=school_query.values('short_name'),
            academic_year__name=academic_year_query.values('name'),
            teacher__firstname=employee_query.values('person__firstname'),
            teacher__surname=employee_query.values('person__surname'),
            teacher__patronymic=employee_query.values('person__patronymic'),
            parallel__title=parallel_query.values('title'),
        )
