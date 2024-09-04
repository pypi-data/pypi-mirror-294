from typing import (
    Any,
)

from django.db.models import (
    F,
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

from edulib.core.lib_passport.cleanup_days.domain import (
    CreateCleanupDay,
    DeleteCleanupDay,
)
from edulib.core.lib_passport.cleanup_days.models import (
    CleanupDays,
)
from edulib.core.lib_passport.documents.domain import (
    CreateDocument,
    DeleteDocument,
    UpdateDocument,
)
from edulib.core.lib_passport.documents.models import (
    LibPassportDocuments,
)
from edulib.core.lib_passport.domain import (
    CreatePassport,
    CreateWorkMode,
    DeletePassport,
    DeleteWorkMode,
    UpdatePassport,
    UpdateWorkMode,
)
from edulib.core.lib_passport.models import (
    LibPassport,
    WorkMode,
)
from edulib.rest.base.mixins import (
    CommandBasedCreateModelMixin,
    CommandBasedDestroyModelMixin,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.passports.filters import (
    PassportFilter,
)
from edulib.rest.passports.serializers import (
    CleanupDaySerializer,
    DocumentSerializer,
    PassportReadSerializer,
    PassportSerializer,
    WorkModeSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)
from edulib.rest.utils.tools import (
    get_person_short_name,
)


class PassportViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с паспортом библиотеки."""

    queryset = LibPassport.objects.select_related('library_chief', 'address').all()
    pagination_class = LimitOffsetPagination
    parser_classes = (MultiPartParser,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = PassportFilter
    search_fields = ('name', )

    create_command = CreatePassport
    update_command = UpdatePassport
    delete_command = DeletePassport

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PassportReadSerializer
        return PassportSerializer

    def get_queryset(self):
        query = super().get_queryset()
        if self.action in ('list', 'retrieve'):
            query = query.annotate(
                employee_id=F('library_chief__id'),
                short_name=get_person_short_name('library_chief__person'),
                lib_address_id=F('address__id'),
                full_address=F('address__full')
            )
        return query


class WorkModeViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с режимом работы библиотеки."""

    queryset = WorkMode.objects.none()
    serializer_class = WorkModeSerializer

    create_command = CreateWorkMode
    update_command = UpdateWorkMode
    delete_command = DeleteWorkMode

    def get_queryset(self) -> Any:
        lib_passport_id = self.kwargs['lib_passport_id']
        return WorkMode.objects.filter(lib_passport_id=lib_passport_id)

    def prepare_additional_create_command_data(self, request, *args, **kwargs):
        return {
            'lib_passport_id': kwargs.get('lib_passport_id'),
        }


class DocumentViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с документами библиотеки."""

    queryset = LibPassportDocuments.objects.none()
    serializer_class = DocumentSerializer
    pagination_class = LimitOffsetPagination

    create_command = CreateDocument
    update_command = UpdateDocument
    delete_command = DeleteDocument

    def get_queryset(self):
        library_passport_id = self.kwargs['lib_passport_id']
        return LibPassportDocuments.objects.filter(library_passport_id=library_passport_id)

    def prepare_additional_create_command_data(self, request, *args, **kwargs):
        return {
            'library_passport_id': kwargs.get('lib_passport_id'),
        }


class CleanupDayViewSet(
    CommandBasedCreateModelMixin,
    CommandBasedDestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """Эндпоинты для работы с санитарными днями библиотеки."""

    queryset = CleanupDays.objects.none()
    serializer_class = CleanupDaySerializer
    create_command = CreateCleanupDay
    delete_command = DeleteCleanupDay

    def get_queryset(self):
        lib_passport_id = self.kwargs['lib_passport_id']
        return CleanupDays.objects.filter(lib_passport_id=lib_passport_id)

    def prepare_additional_create_command_data(self, request, *args, **kwargs):
        return {
            'lib_passport_id': kwargs.get('lib_passport_id'),
        }
