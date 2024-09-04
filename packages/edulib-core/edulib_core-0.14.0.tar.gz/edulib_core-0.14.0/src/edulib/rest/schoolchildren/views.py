from django.db.models import (
    OuterRef,
    Q,
    Subquery,
)
from django.utils import (
    timezone,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

from edulib.core.classyears.models import (
    ClassYear,
)
from edulib.core.genders.models import (
    Gender,
)
from edulib.core.persons.models import (
    Person,
)
from edulib.core.pupils.models import (
    Pupil,
)
from edulib.core.schoolchildren.models import (
    Schoolchild,
)
from edulib.core.schools.models import (
    School,
)
from edulib.rest.schoolchildren.filters import (
    SchoolchildFilter,
)
from edulib.rest.schoolchildren.serializers import (
    SchoolchildSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class SchoolchildViewSet(ReadOnlyModelViewSet):
    """Эндпоинты для работы с учащимися."""

    queryset = Schoolchild.objects.none()
    serializer_class = SchoolchildSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filterset_class = SchoolchildFilter
    search_fields = ('person_firstname', 'person_surname', 'person_patronymic', 'pupil_school_short_name')

    def get_queryset(self):
        now = timezone.now()
        person_subquery = Person.objects.filter(id=OuterRef('person_id')).values(
            'id', 'surname', 'firstname', 'patronymic', 'date_of_birth', 'gender_id'
        )

        gender_subquery = Gender.objects.filter(id=OuterRef('person_gender_id')).values('name')

        pupil_query = Pupil.objects.filter(
            Q(training_end_date__gt=now) | Q(training_end_date__isnull=True),
            training_begin_date__lte=now,
            schoolchild_id=OuterRef('id')
        ).order_by('-training_begin_date').annotate(
            class_year_name=Subquery(ClassYear.objects.filter(id=OuterRef('class_year_id')).values('name')[:1]),
            school_short_name=Subquery(School.objects.filter(id=OuterRef('school_id')).values('short_name')[:1])
        ).values(
            'id', 'class_year_id', 'class_year_name', 'school_id', 'school_short_name', 'training_begin_date',
            'training_end_date'
        )

        queryset = Schoolchild.objects.annotate(
            person_id_annotate=Subquery(person_subquery.values('id')[:1]),
            person_surname=Subquery(person_subquery.values('surname')[:1]),
            person_firstname=Subquery(person_subquery.values('firstname')[:1]),
            person_patronymic=Subquery(person_subquery.values('patronymic')[:1]),
            person_date_of_birth=Subquery(person_subquery.values('date_of_birth')[:1]),
            person_gender_id=Subquery(person_subquery.values('gender_id')[:1]),
            person_gender_name=Subquery(gender_subquery[:1]),
            pupil_id=Subquery(pupil_query.values('id')[:1]),
            pupil_class_year_id=Subquery(pupil_query.values('class_year_id')[:1]),
            pupil_class_year_name=Subquery(pupil_query.values('class_year_name')[:1]),
            pupil_school_id=Subquery(pupil_query.values('school_id')[:1]),
            pupil_school_short_name=Subquery(pupil_query.values('school_short_name')[:1]),
            pupil_training_begin_date=Subquery(pupil_query.values('training_begin_date')[:1]),
            pupil_training_end_date=Subquery(pupil_query.values('training_end_date')[:1])
        )

        return queryset
