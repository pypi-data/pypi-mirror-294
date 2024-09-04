from django_filters import (
    rest_framework as filters,
)

from edulib.core.federal_books import (
    domain,
)
from edulib.core.federal_books.models import (
    FederalBook,
)


class FederalBookFilter(filters.FilterSet):
    author_id = filters.NumberFilter(field_name='author_id', lookup_expr='exact')
    publishing_id = filters.NumberFilter(field_name='publishing_id', lookup_expr='exact')
    status = filters.BooleanFilter(field_name='status', lookup_expr='exact')

    ordering = filters.OrderingFilter(
        fields=(
            ('author', 'author'),
            ('code', 'code'),
            ('name', 'name'),
            ('parallel', 'parallel'),
            ('publishing', 'publishing'),
            ('pub_lang', 'pub_lang'),
            ('status', 'status'),
            ('validity_period', 'validity_period'),
        ),
        field_labels={
            'author': domain.FederalBook.authors.title,
            'code': domain.FederalBook.code.title,
            'name': domain.FederalBook.name.title,
            'parallel': domain.FederalBook.parallel_ids.title,
            'publishing': domain.FederalBook.publishing_id.title,
            'pub_lang': domain.FederalBook.pub_lang.title,
            'status': domain.FederalBook.status.title,
            'validity_period': domain.FederalBook.validity_period.title,
        },
    )

    class Meta:
        model = FederalBook
        fields = [
            'pub_lang',
        ]
