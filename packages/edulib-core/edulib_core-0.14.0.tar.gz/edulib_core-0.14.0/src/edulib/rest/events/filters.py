from django_filters import (
    rest_framework as filters,
)

from edulib.core.library_event import (
    domain,
)
from edulib.core.library_event.models import (
    LibraryEvent,
)


class EventFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('place', 'place'),
            ('participants', 'participants'),
            ('date_begin', 'date_begin'),
        ),
        field_labels={
            'name': domain.Event.name.title,
            'place': domain.Event.place.title,
            'participants': domain.Event.participants.title,
            'date_begin': domain.Event.date_begin.title,
        },
    )

    class Meta:
        model = LibraryEvent
        fields = []
