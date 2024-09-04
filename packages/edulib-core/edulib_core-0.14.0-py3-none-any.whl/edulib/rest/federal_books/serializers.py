from rest_framework.serializers import (
    FileField,
    ModelSerializer,
    Serializer,
    ValidationError,
)

from edulib.core.federal_books.models import (
    FederalBook,
)
from edulib.rest.authors.serializers import (
    AuthorSerializer,
)
from edulib.rest.publishings.serializers import (
    PublishingSerializer,
)


class FederalBookSerializer(ModelSerializer):
    author = AuthorSerializer()
    publishing = PublishingSerializer()

    class Meta:
        model = FederalBook
        fields = (
            'id',
            'name',
            'author',
            'publishing',
            'pub_lang',
            'status',
            'code',
            'validity_period',
            'training_manuals',
            'parallel',
        )


class FileUploadSerializer(Serializer):
    file = FileField()

    def validate(self, data):
        file = data.get('file')
        if not file:
            raise ValidationError("Файл не найден.")

        if not file.name.endswith('.xlsx'):
            raise ValidationError("Приложен некорректный тип файла.")

        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
