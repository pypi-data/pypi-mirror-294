from django.db.models import (
    CharField,
    DateField,
    ExpressionWrapper,
    F,
    IntegerField,
    OuterRef,
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
from explicit.django.domain.validation.exceptions import (
    handle_domain_validation_error,
)
from rest_framework import (
    mixins,
    status,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    GenericViewSet,
)

from edulib.core import (
    bus,
)
from edulib.core.employees.models import (
    Employee,
)
from edulib.core.issuance_delivery import (
    domain,
)
from edulib.core.issuance_delivery.models import (
    IssuanceDelivery,
)
from edulib.core.persons.models import (
    Person,
)
from edulib.core.schoolchildren.models import (
    Schoolchild,
)
from edulib.rest.base.decorators import (
    handle_django_validation_error,
)
from edulib.rest.issuance_delivery.filters import (
    IssuanceDeliveryFilter,
)
from edulib.rest.issuance_delivery.serializers import (
    AutoIssueExamplesSerializer,
    DeliverExamplesSerializer,
    IssuanceDeliveryOutputSerializer,
    IssuanceDeliverySerializer,
    IssueExamplesSerializer,
    ProlongIssuanceSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class IssuanceDeliveryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """Эндпоинты для работы с выдачей/сдачей экземпляров библиотечных изданий."""

    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = IssuanceDeliveryFilter
    search_fields = (
        'example__lib_reg_entry__title',
        'example__card_number',
        'issuance_date',
        'plan_del_date',
    )

    def get_queryset(self):
        schoolchild_query = Schoolchild.objects.filter(id=OuterRef('reader__schoolchild_id'))
        employee_query = Employee.objects.filter(id=OuterRef('reader__teacher_id'))
        person_query = Person.objects.filter(id=OuterRef('person_id'))

        return IssuanceDelivery.objects.select_related('example__lib_reg_entry__author', 'reader').annotate(
            person_id=Coalesce(
                schoolchild_query.values('person_id'),
                employee_query.values('person_id'),
                output_field=CharField(),
            ),
            firstname=person_query.values('firstname'),
            surname=person_query.values('surname'),
            patronymic=person_query.values('patronymic'),
            plan_del_date=ExpressionWrapper(
                F('issuance_date')
                + timezone.timedelta(days=1)
                * (
                    Coalesce(F('extension_days_count'), 0)
                    + Coalesce(Cast('example__max_date', output_field=IntegerField()), 0)
                ),
                output_field=DateField(),
            ),
        )

    @handle_django_validation_error
    @handle_domain_validation_error
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        command = domain.IssueExamples(**serializer.validated_data)

        result = bus.handle(command)

        return Response(data=IssuanceDeliveryOutputSerializer(result, many=True).data, status=status.HTTP_201_CREATED)

    @handle_django_validation_error
    @handle_domain_validation_error
    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        command = domain.ProlongIssuance(id=kwargs.get(self.lookup_field), **serializer.validated_data)

        result = bus.handle(command)

        return Response(data=IssuanceDeliveryOutputSerializer(result).data, status=status.HTTP_200_OK)

    @handle_django_validation_error
    @handle_domain_validation_error
    @action(detail=False, methods=['post'], url_path='return', url_name='return')
    def return_example(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        command = domain.DeliverExamples(**serializer.validated_data)

        result = bus.handle(command)

        return Response(data=IssuanceDeliveryOutputSerializer(result, many=True).data, status=status.HTTP_200_OK)

    @handle_django_validation_error
    @handle_domain_validation_error
    @action(detail=False, methods=['post'], url_path='auto', url_name='auto')
    def auto(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        command = domain.AutoIssueExamples(**serializer.validated_data)

        result = bus.handle(command)

        return Response(data=IssuanceDeliveryOutputSerializer(result, many=True).data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create':
            return IssueExamplesSerializer
        if self.action == 'return_example':
            return DeliverExamplesSerializer
        if self.action == 'partial_update':
            return ProlongIssuanceSerializer
        if self.action == 'auto':
            return AutoIssueExamplesSerializer

        return IssuanceDeliverySerializer
