from typing import (
    TYPE_CHECKING,
)

from django.db.models import (
    CharField,
    Count,
    DateField,
    ExpressionWrapper,
    F,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
)
from django.db.models.functions import (
    Cast,
    Coalesce,
)
from django.utils import (
    timezone,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework import (
    mixins,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.viewsets import (
    GenericViewSet,
)

from edulib.core.classyears.models import (
    ClassYear,
)
from edulib.core.employees.models import (
    Employee,
)
from edulib.core.issuance_delivery.models import (
    IssuanceDelivery,
)
from edulib.core.persons.models import (
    Person,
)
from edulib.core.pupils.models import (
    Pupil,
)
from edulib.core.readers.domain.commands import (
    UpdateReader,
)
from edulib.core.readers.models import (
    Reader,
)
from edulib.core.schoolchildren.models import (
    Schoolchild,
)
from edulib.core.schools.models import (
    School,
)
from edulib.rest.base.mixins import (
    CommandBasedUpdateModelMixin,
)
from edulib.rest.readers.filters import (
    ReaderFilter,
)
from edulib.rest.readers.serializers import (
    ReaderSerializer,
    ReaderUpdateSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


if TYPE_CHECKING:
    from django.db.models import (
        QuerySet,
    )
    from rest_framework.serializers import (
        Serializer,
    )


class ReaderViewSet(
    mixins.RetrieveModelMixin,
    CommandBasedUpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = ReaderFilter
    search_fields = (
        'number',
        'firstname',
        'surname',
        'patronymic',
    )

    update_command = UpdateReader

    def get_queryset(self) -> 'QuerySet[Reader]':
        now = timezone.now()
        schoolchild_query = Schoolchild.objects.filter(id=OuterRef('schoolchild_id'))
        employee_query = Employee.objects.filter(id=OuterRef('teacher_id'))
        person_query = Person.objects.filter(id=OuterRef('person_id'))
        school_query = School.objects.filter(id=OuterRef('dependent_school_id'))
        class_year_query = ClassYear.objects.filter(id=OuterRef('class_year_id'))
        class_year_query_for_employee = ClassYear.objects.filter(teacher_id=OuterRef('teacher_id'))

        pupil_query = Pupil.objects.filter(
            Q(training_end_date__gt=now) | Q(training_end_date__isnull=True),
            training_begin_date__lte=now,
            schoolchild_id=OuterRef('schoolchild_id'),
        ).order_by('-training_begin_date')

        # Подсчет просроченных экземпляров (в fact_delivery_date пусто, а дата возврата в plan_del_date уже прошла)
        overdue_examples_count_query = IssuanceDelivery.objects.filter(
            reader_id=OuterRef('id'),
            fact_delivery_date__isnull=True
        ).annotate(
            plan_del_date=ExpressionWrapper(
                F('issuance_date')
                + timezone.timedelta(days=1)
                * (
                        Coalesce(F('extension_days_count'), 0)
                        + Coalesce(Cast('example__max_date', output_field=IntegerField()), 0)
                ),
                output_field=DateField(),
            )
        ).filter(
            plan_del_date__lt=now
        ).values('reader_id').annotate(count=Count('id')).values('count')

        return Reader.objects.annotate(
            person_id=Coalesce(
                schoolchild_query.values('person_id'),
                employee_query.values('person_id'),
                output_field=CharField(),
            ),
            firstname=person_query.values('firstname'),
            surname=person_query.values('surname'),
            patronymic=person_query.values('patronymic'),
            dependent_school_id=Coalesce(
                employee_query.values('school_id'),
                pupil_query.values('school_id')[:1],
            ),
            school_shortname=school_query.values('short_name'),
            class_year_id=Coalesce(
                pupil_query.values('class_year_id')[:1],
                class_year_query_for_employee.values('id')[:1],
            ),
            class_year_name=Coalesce(
                class_year_query.values('name'),
                class_year_query_for_employee.values('name'),
            ),
            overdue_examples_count=Coalesce(Subquery(overdue_examples_count_query), 0),
        )

    def get_serializer_class(self) -> type['Serializer']:
        if self.action in {'list', 'retrieve'}:
            return ReaderSerializer

        return ReaderUpdateSerializer
