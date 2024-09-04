from typing import (
    Generator,
)

from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.forms import (
    model_to_dict,
)
from explicit.adapters.db import (
    AbstractRepository,
)

from edulib.core.federal_books import (
    models as db,
)
from edulib.core.federal_books.domain.model import (
    FederalBook,
    FederalBookNotFound,
)


class FederalBookRepository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> FederalBook:
        """Получает объект по идентификатору."""
        try:
            db_instance = db.FederalBook.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as e:
            raise FederalBookNotFound() from e

    def add(self, obj: FederalBook) -> FederalBook:
        assert isinstance(obj, FederalBook)

        return self._to_db(obj)

    def update(self, obj: FederalBook) -> FederalBook:
        assert isinstance(obj, FederalBook)

        return self._to_db(obj)

    def delete(self, obj: FederalBook) -> None:
        assert isinstance(obj, FederalBook)
        db.FederalBook.objects.get(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[FederalBook, None, None]:
        for federal_book in db.FederalBook.objects.iterator():
            yield self._to_domain(federal_book)

    def federal_book_exists(self, federal_book: FederalBook) -> bool:
        """Проверяет существование учебника в Федеральном перечне учебников."""
        books = db.FederalBook.objects.exclude(pk=federal_book.id).filter(
            name__iexact=federal_book.name,
            author=federal_book.authors,
            publishing=federal_book.publishing_id
        )

        # Подсчитываем количество книг с точно таким же набором параллелей
        # Предполагается, что каждая книга имеет связь many-to-many с параллелями через 'parallel'
        for book in books:
            book_parallel_ids = set(book.parallel.all().values_list('id', flat=True))
            if book_parallel_ids == set(federal_book.parallel_ids):
                return True

        return False

    def get_or_create_by_name(self, federal_book: FederalBook):
        defaults = {
            'name': federal_book.name,
            'pub_lang': federal_book.pub_lang,
            'status': federal_book.status,
            'code': federal_book.code,
            'validity_period': federal_book.validity_period,
            'training_manuals': federal_book.training_manuals,
        }

        db_instance, _ = db.FederalBook.objects.get_or_create(
            publishing_id=federal_book.publishing_id,
            author_id=federal_book.authors,
            defaults=defaults
        )

        db_instance.parallel.set(
            parallel
            for parallel in federal_book.parallel_ids
        )

        return self._to_domain(db_instance)

    def _to_db(self, federal_book: FederalBook) -> FederalBook:
        assert isinstance(federal_book, FederalBook)

        defaults = {
            'name': federal_book.name,
            'pub_lang': federal_book.pub_lang,
            'status': federal_book.status,
            'code': federal_book.code,
            'validity_period': federal_book.validity_period,
            'training_manuals': federal_book.training_manuals,
        }

        db_instance, _ = db.FederalBook.objects.update_or_create(
            pk=federal_book.id,
            publishing_id=federal_book.publishing_id,
            author_id=federal_book.authors,
            defaults=defaults
        )

        db_instance.parallel.set(
            parallel
            for parallel in federal_book.parallel_ids
        )

        federal_book.id = db_instance.pk

        return federal_book

    def _to_domain(self, dbinstance: db.FederalBook) -> FederalBook:
        result = FederalBook(
            publishing_id=dbinstance.publishing_id,
            authors=dbinstance.author_id,
            **model_to_dict(dbinstance, exclude=['publishing', 'authors', 'parallel_ids'])
        )

        result.parallel_ids = list(dbinstance.parallel.all().values_list('id', flat=True))

        return result


repository = FederalBookRepository()
