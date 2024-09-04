from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.parsers import (
    MultiPartParser,
)

from edulib.core.library_event import (
    domain,
)
from edulib.core.library_event.models import (
    LibraryEvent,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.events.filters import (
    EventFilter,
)
from edulib.rest.events.serializers import (
    EventSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class EventViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с планами работы библиотеки."""

    queryset = LibraryEvent.objects.all()
    serializer_class = EventSerializer
    pagination_class = LimitOffsetPagination
    parser_classes = (MultiPartParser,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = EventFilter
    search_fields = ('name', 'place', 'participants', 'date_begin')

    create_command = domain.CreateEvent
    update_command = domain.UpdateEvent
    delete_command = domain.DeleteEvent
