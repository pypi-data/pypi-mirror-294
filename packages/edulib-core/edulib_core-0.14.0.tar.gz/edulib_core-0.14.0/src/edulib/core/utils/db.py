import re

from django.db.models import (
    Func,
)


def normalize_string(s):
    """Удаляет спецсимволы, пробелы, приводит строку к нижнему регистру."""
    return re.sub(r'[^\w]+', '', s).lower().replace(" ", "")


class StripChars(Func):  # pylint: disable=abstract-method
    """SQL-функция для Django ORM, которая применяет замену по регулярному выражению
    к указанному полю. Для удаления или замены символов согласно указанному
    шаблону с использованием функции REGEXP_REPLACE в PostgreSQL."""
    function = 'REGEXP_REPLACE'
    template = "%(function)s(%(expressions)s, '%(pattern)s', '%(replacement)s', 'g')"

    def __init__(self, expression, pattern=None, replacement=''):
        super().__init__(
            expression,
            pattern=pattern,
            replacement=replacement
        )
