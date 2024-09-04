import pandas as pd
from django_filters.rest_framework import (
    DjangoFilterBackend,
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
from rest_framework.parsers import (
    MultiPartParser,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    GenericViewSet,
)

from edulib.core.federal_books.models import (
    FederalBook,
)
from edulib.core.federal_books.services.validators import (
    validate_file,
)
from edulib.rest.federal_books.filters import (
    FederalBookFilter,
)
from edulib.rest.federal_books.serializers import (
    FederalBookSerializer,
    FileUploadSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)
from edulib.rest.utils.utils import (
    create_log_response,
)


class FederalBookViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """Эндпоинты для отображения Федерального перечня учебников"""

    queryset = FederalBook.objects.select_related('author', 'publishing').prefetch_related('parallel').all()
    serializer_class = FederalBookSerializer
    pagination_class = LimitOffsetPagination
    parser_classes = (MultiPartParser,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = FederalBookFilter
    search_fields = ('author__name', 'code', 'name', 'parallel__title', 'publishing__name', 'validity_period')

    def get_serializer_class(self):
        if self.action == 'import_books':
            return FileUploadSerializer
        return FederalBookSerializer

    @action(detail=False, methods=['post'], url_path='import', parser_classes=[MultiPartParser])
    def import_books(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            try:
                df = pd.read_excel(file)
            except pd.errors.EmptyDataError:
                return Response({"error": "Файл пуст."}, status=status.HTTP_400_BAD_REQUEST)
            except pd.errors.ParserError:
                return Response({"error": "Ошибка парсинга данных в файле."}, status=status.HTTP_400_BAD_REQUEST)

            log_changes, cleaned_df = validate_file(df)  # pylint: disable=unused-variable

            # Placeholder for further processing with cleaned_df in EDUBOOKS-38
            # process_log = self.process_file(cleaned_df)
            # log_changes.extend(process_log)

            return create_log_response(log_changes, status_code=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
