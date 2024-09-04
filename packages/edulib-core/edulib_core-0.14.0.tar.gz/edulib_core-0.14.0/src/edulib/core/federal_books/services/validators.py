from typing import (
    Optional,
)

import pandas as pd

from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.federal_books.constants import (
    COLUMN_AUTHOR,
    COLUMN_CLASS,
    COLUMN_NAME,
    COLUMN_PUBLISHER,
    COLUMN_ROW_NUM,
    REQUIRED_COLUMNS,
)
from edulib.core.federal_books.domain import (
    FederalBook,
    FederalBookNotFound,
    factory,
)


class FederalBookValidator(Validator):
    """Валидатор учебника из Федерального перечня учебников."""

    def validate_existence(self) -> 'FederalBookValidator':
        if not self._get_federal_book(self._data.id, 'id'):
            self._skip_chain = True

        return self

    @may_skip
    def validate_parallels(self) -> 'FederalBookValidator':
        existing_parallels = self._uow.parallels.get_objects_by_ids(self._data.parallel_ids)
        existing_parallel_ids = {p.id for p in existing_parallels}
        missing_ids = set(self._data.parallel_ids) - existing_parallel_ids
        if missing_ids:
            self._errors['parallel_ids'].append(f"Не найдены параллели с ID: {missing_ids}")

        return self

    @may_skip
    def validate_federal_book(self, *, is_update: bool = False) -> 'FederalBookValidator':
        if 'name' in self._data.dict() and 'authors' in self._data.dict():
            name = self._data.name.strip()
            authors = self._data.authors
            if name and authors:
                federal_book = factory.create(self._data)
                if self._uow.federal_books.federal_book_exists(federal_book):
                    self._errors['name'].append('Такой учебник уже существует в Федеральном перечне учебников')
        return self

    def _get_federal_book(self, identifier: int, error_name: str) -> Optional[FederalBook]:
        try:
            return self._uow.federal_books.get_object_by_id(identifier)
        except FederalBookNotFound as exc:
            self._errors[error_name].append(str(exc))


def validate_file(df):
    log_changes = []
    cleaned_df = df.copy()

    # Проверяем, чтобы в обязательных
    for index, row in df.iterrows():
        row_num = row[COLUMN_ROW_NUM]
        for col in REQUIRED_COLUMNS:
            if pd.isna(row[col]):
                log_changes.append(f"Ошибка: Строка {row_num} не указан обязательный атрибут {col}")
                cleaned_df.drop(index, inplace=True)
                break

    # Check for duplicates
    seen = {}
    for index, row in cleaned_df.iterrows():
        row_num = row[COLUMN_ROW_NUM]
        identifier = (
            row[COLUMN_NAME],
            row[COLUMN_AUTHOR],
            row[COLUMN_CLASS],
            row[COLUMN_PUBLISHER]
        )
        if identifier in seen:
            original_row_num = seen[identifier]
            log_changes.append(
                f"Ошибка: Строка {row_num} является дублем строки {original_row_num}. Запись будет пропущена"
            )
            cleaned_df.drop(index, inplace=True)
        else:
            seen[identifier] = row_num

    return log_changes, cleaned_df
