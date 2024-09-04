from typing import (
    TYPE_CHECKING,
)

from django.contrib.postgres.aggregates import (
    StringAgg,
)
from django.db.models import (
    Case,
    CharField,
    Count,
    ExpressionWrapper,
    F,
    FloatField,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import (
    Cast,
    Coalesce,
    Round,
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
from rest_framework.parsers import (
    MultiPartParser,
)
from rest_framework.viewsets import (
    GenericViewSet,
)

from edulib.core.classyears.models import (
    ClassYear,
)
from edulib.core.disciplines.models import (
    Discipline,
)
from edulib.core.lib_registry.domain.commands import (
    CreateRegistryEntry,
    DeleteRegistryEntry,
    UpdateRegistryEntry,
)
from edulib.core.lib_registry.models import (
    LibRegistryEntry,
    RegistryEntryParallel,
)
from edulib.core.municipal_units.models import (
    MunicipalUnit,
)
from edulib.core.pupils.models import (
    Pupil,
)
from edulib.core.schools.models import (
    School,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.registry_entries.filters import (
    EntryFilter,
    GeneralFundFilter,
)
from edulib.rest.registry_entries.serializers import (
    EntryListSerializer,
    EntryRetrieveSerializer,
    EntrySerializer,
    GeneralFundSerializer,
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


def get_entry_queryset() -> 'QuerySet[LibRegistryEntry]':
    return LibRegistryEntry.objects.select_related(
        'author', 'type', 'udc', 'bbc', 'source', 'age_tag',
    ).annotate(
        discipline_name=Discipline.objects.filter(id=OuterRef('discipline_id')).values('name')[:1],
        editions=StringAgg('examples__edition', delimiter=', ', distinct=True),
        publishings=StringAgg('examples__publishing__name', delimiter=', ', distinct=True),
        publishing_years=StringAgg(
            Cast('examples__edition_year', CharField()),
            delimiter=', ',
            distinct=True,
        ),
        count=Count(
            'examples',
            filter=Q(
                Q(examples__writeoff_date__isnull=True)
                | Q(examples__writeoff_date__gt=timezone.now()),
            ),
        ),
        free_count=Count(
            'examples',
            filter=Q(
                Q(examples__writeoff_date__isnull=True)
                | Q(examples__writeoff_date__gt=timezone.now()),
                Q(examples__issuancedelivery__fact_delivery_date__isnull=True)
                | Q(examples__issuancedelivery__fact_delivery_date__lt=timezone.now()),
            ),
        ),
    ).all()


class EntryViewSet(CommandBasedModelViewSet):
    queryset = LibRegistryEntry.objects.none()
    parser_classes = (MultiPartParser,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = EntryFilter
    search_fields = ('title',)

    create_command = CreateRegistryEntry
    update_command = UpdateRegistryEntry
    delete_command = DeleteRegistryEntry

    def get_queryset(self) -> 'QuerySet[LibRegistryEntry]':
        return get_entry_queryset()

    def get_serializer_class(self) -> type['Serializer']:
        if self.action == 'list':
            return EntryListSerializer
        if self.action == 'retrieve':
            return EntryRetrieveSerializer

        return EntrySerializer



class GeneralFundViewSet(mixins.ListModelMixin, GenericViewSet):
    """Эндпоинты для работы с Общим фондом литературы."""

    queryset = LibRegistryEntry.objects.none()
    serializer_class = GeneralFundSerializer
    parser_classes = (MultiPartParser,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = GeneralFundFilter
    search_fields = ('title',)

    def get_queryset(self):
        registry_entry_parallels = RegistryEntryParallel.objects.annotate(
            parallel_id_bigint=Cast('parallel_id', IntegerField())
        ).values('parallel_id_bigint')

        class_year_ids = ClassYear.objects.filter(
            school_id=OuterRef('school_id'),
            parallel_id__in=Subquery(registry_entry_parallels)
        ).values('id')

        school_subquery = School.objects.filter(
            id=OuterRef('school_id')
        ).values('id', 'name', 'municipal_unit_id')

        municipal_unit_name = Subquery(
            MunicipalUnit.objects.filter(
                id=OuterRef('municipal_unit_id')
            ).values('name')[:1], output_field=CharField()
        )

        student_count = Coalesce(
            Subquery(
                Pupil.objects.filter(
                    Q(school_id=OuterRef('school_id')),
                    Q(training_end_date__isnull=True) | Q(training_end_date__gt=timezone.now()),
                    Q(class_year_id__in=Subquery(class_year_ids))
                )
                .values('school_id')
                .annotate(student_count=Count('id'))
                .values('student_count')[:1]
            ),
            0
        )

        return get_entry_queryset().prefetch_related('parallels').annotate(
            school_name=Subquery(school_subquery.values('name')[:1], output_field=CharField()),
            municipal_unit_id=Cast(
                Subquery(school_subquery.values('municipal_unit_id')[:1]),
                output_field=IntegerField(),
            ),
            municipal_unit_name=municipal_unit_name,
            student_count=student_count,
            lack=Case(
                When(
                    student_count__gt=F('count'),
                    then=F('student_count') - F('count'),
                ),
                default=Value(None),
                output_field=IntegerField(),
            ),
            excess=Case(
                When(
                    student_count__lt=F('count'),
                    then=F('count') - F('student_count'),
                ),
                default=Value(None),
                output_field=IntegerField(),
            ),
            sufficiency=Case(
                When(
                    student_count__gt=0,
                    then=Round(
                        ExpressionWrapper(
                            (F('count') * 100.0 / F('student_count')),
                            output_field=FloatField(),
                        ),
                        precision=2,
                    ),
                ),
                default=Value(100),
                output_field=FloatField(),
            ),
        )
