from typing import (
    TYPE_CHECKING,
)

from explicit.domain import (
    DTOBase,
    asdict,
)

from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.directory.domain import (
    BbkNotFound,
)
from edulib.core.disciplines.domain import (
    DisciplineNotFound,
)
from edulib.core.federal_books.domain.model import (
    FederalBookNotFound,
)
from edulib.core.lib_authors.domain import (
    AuthorNotFound,
)
from edulib.core.lib_example_types.domain import (
    CLASSBOOK_ID,
    ExampleTypeNotFound,
)
from edulib.core.lib_publishings.domain import (
    PublishingNotFound,
)
from edulib.core.lib_registry.domain import (
    InfoProductMarkNotFound,
    RegistryEntry,
    RegistryEntryDTO,
    RegistryEntryNotFound,
    entry_factory,
)
from edulib.core.lib_registry.domain.model import (
    RegistryExampleNotFound,
)
from edulib.core.lib_sources.domain import (
    SourceNotFound,
)
from edulib.core.lib_udc.domain import (
    UdcNotFound,
)
from edulib.core.schools.domain.model import (
    SchoolNotFound,
)
from edulib.core.unit_of_work import (
    UnitOfWork,
)


if TYPE_CHECKING:
    from explicit.adapters.db import (
        AbstractRepository,
    )


class RegistryEntryValidator(Validator):
    def __init__(self, data: DTOBase, uow: UnitOfWork) -> None:
        super().__init__(data, uow)

        self._registry_entry = None
        self._federal_book = None

    def validate_existence(self) -> 'RegistryEntryValidator':
        try:
            self._registry_entry = self._uow.registry_entries.get_object_by_id(self._data.id)
        except RegistryEntryNotFound as exc:
            self._errors['id'].append(str(exc))
            self._skip_chain = True

        return self

    def validate(self) -> 'RegistryEntryValidator':
        return (
            self.validate_bbc()
            .validate_udc()
            .validate_discipline()
            .validate_type()
            .validate_author()
            .validate_source()
            .validate_age_tag()
            .validate_school()
            .validate_parallels()
            .validate_federal_book()
            .validate_federal_book_relevant_type()
            .validate_similar()
            .validate_required_fields()
        )

    @may_skip
    def validate_examples(self) -> 'RegistryEntryValidator':
        if self._uow.registry_entries.has_examples(self._registry_entry):
            self._errors['__root__'].append('Невозможно удалить библиотечное издание, т.к. имеются экземпляры')

        return self

    def validate_bbc(self) -> 'RegistryEntryValidator':
        return self._validate_relation('bbc_id', self._uow.bbk, BbkNotFound)

    def validate_udc(self) -> 'RegistryEntryValidator':
        return self._validate_relation('udc_id', self._uow.udc, UdcNotFound)

    def validate_discipline(self) -> 'RegistryEntryValidator':
        return self._validate_relation('discipline_id', self._uow.disciplines, DisciplineNotFound)

    def validate_type(self) -> 'RegistryEntryValidator':
        return self._validate_relation('type_id', self._uow.example_types, ExampleTypeNotFound)

    def validate_author(self) -> 'RegistryEntryValidator':
        return self._validate_relation('author_id', self._uow.authors, AuthorNotFound)

    def validate_source(self) -> 'RegistryEntryValidator':
        return self._validate_relation('source_id', self._uow.sources, SourceNotFound)

    def validate_age_tag(self) -> 'RegistryEntryValidator':
        return self._validate_relation('age_tag_id', self._uow.info_product_marks, InfoProductMarkNotFound)

    def validate_school(self) -> 'RegistryEntryValidator':
        return self._validate_relation('school_id', self._uow.schools, SchoolNotFound, skip_chain=True)

    def validate_federal_book(self) -> 'RegistryEntryValidator':
        if self._data.federal_book_id:
            try:
                self._federal_book = self._uow.federal_books.get_object_by_id(self._data.federal_book_id)
            except FederalBookNotFound as exc:
                self._errors['federal_book_id'].append(str(exc))
                self._skip_chain = True

        return self

    @may_skip
    def validate_federal_book_relevant_type(self) -> 'RegistryEntryValidator':
        registry_entry = self._create_registry_entry()
        if registry_entry.federal_book_id and registry_entry.type_id != CLASSBOOK_ID:
            self._errors['type_id'].append(
                'Учебник федерального перечня может быть указан только для '
                'типа библиотечного издания "Учебник, учебная литература"'
            )

        return self

    @may_skip
    def validate_required_fields(self) -> 'RegistryEntryValidator':
        registry_entry = self._create_registry_entry()
        if not any((registry_entry.federal_book_id, all((registry_entry.title, registry_entry.author_id)))):
            self._errors['__root__'].append(
                'Необходимо указать наименование и автора, либо учебник федерального перечня'
            )

        return self

    @may_skip
    def validate_similar(self) -> 'RegistryEntryValidator':
        if any((self._data.title, self._data.author_id, self._data.federal_book_id)):
            registry_entry = self._create_registry_entry()
            if self._uow.registry_entries.has_similar(registry_entry, self._federal_book):
                self._errors['__root__'].append('Такое библиотечное издание уже существует')

        return self

    def validate_parallels(self) -> 'RegistryEntryValidator':
        if self._data.parallel_ids:
            existing_parallel_ids = {
                parallel.id for parallel in self._uow.parallels.get_objects_by_ids(self._data.parallel_ids)
            }
            if missing_ids := set(self._data.parallel_ids) - existing_parallel_ids:
                self._errors['parallel_ids'].append(f'Не найдены параллели с ID: {", ".join(map(str, missing_ids))}')

        return self

    def _create_registry_entry(self) -> RegistryEntry:
        if self._registry_entry:
            dto = RegistryEntryDTO(**asdict(self._registry_entry) | self._data.dict())
        else:
            dto = self._data

        return entry_factory.create(dto)


class RegistryExampleValidator(Validator):
    def __init__(self, data: DTOBase, uow: UnitOfWork) -> None:
        super().__init__(data, uow)

        self._registry_entry = None
        self._registry_example = None

    def validate_entry(self) -> 'RegistryExampleValidator':
        try:
            self._registry_entry = self._uow.registry_entries.get_object_by_id(self._data.lib_reg_entry_id)
        except RegistryEntryNotFound as exc:
            self._errors['lib_reg_entry_id'].append(str(exc))
            self._skip_chain = True

        return self

    def validate_existence(self) -> 'RegistryExampleValidator':
        try:
            self._registry_example = self._uow.registry_examples.get_object_by_id(self._data.id)
        except RegistryExampleNotFound as exc:
            self._errors['id'].append(str(exc))
            self._skip_chain = True

        return self

    @may_skip
    def validate_publishing(self) -> 'RegistryExampleValidator':
        if publishing_id := self._data.publishing_id:
            try:
                self._uow.publishings.get_object_by_id(publishing_id)
            except PublishingNotFound as exc:
                self._errors['publishing_id'].append(str(exc))

        return self
