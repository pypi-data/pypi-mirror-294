from django.contrib.postgres.aggregates import (
    ArrayAgg,
)
from django.db.models import (
    Case,
    CharField,
    F,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import (
    Coalesce,
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

from edulib.core.address.models import (
    Address,
)
from edulib.core.employees.domain.model import (
    EmploymentKind,
)
from edulib.core.employees.models import (
    Employee,
)
from edulib.core.genders.models import (
    Gender,
)
from edulib.core.schools.models import (
    School,
)
from edulib.rest.employees.filters import (
    EmployeeFilter,
)
from edulib.rest.employees.serializers import (
    EmployeeSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class EmployeeViewSet(ReadOnlyModelViewSet):
    """Эндпоинты для работы с сотрудниками."""

    serializer_class = EmployeeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = EmployeeFilter
    search_fields = ('person__surname', 'person__firstname', 'person__patronymic')

    def get_queryset(self):
        main_employee_query = Employee.objects.filter(
            person_id=OuterRef('person_id'),
            object_status=True,
        ).annotate(
            is_preferred=Case(
                When(employment_kind_id=EmploymentKind.PRIMARY, then=Value(1)),
                default=Value(0),
                output_field=CharField(),
            )
        ).order_by('-is_preferred').values('id')[:1]

        job_names_query = Employee.objects.filter(
            person_id=OuterRef('person_id'),
            object_status=True
        ).values('person_id').annotate(
            job_names=ArrayAgg('job_name', filter=Q(object_status=True), ordering=F('job_name'))
        ).values('job_names')[:1]

        school_query = School.objects.filter(id=OuterRef('school_id'))
        gender_query = Gender.objects.filter(id=OuterRef('person__gender_id'))
        address_query = Address.objects.filter(id=OuterRef('person__temp_reg_addr_id'))

        return Employee.objects.select_related('person').annotate(
            school__short_name=Subquery(school_query.values('short_name')[:1]),
            gender__name=Subquery(gender_query.values('name')[:1]),
            person__full_address=Subquery(address_query.values('full')[:1]),
            main_employee_id=Subquery(main_employee_query),
            job_names=Coalesce(Subquery(job_names_query), Value([])),
        ).filter(id=F('main_employee_id'))
