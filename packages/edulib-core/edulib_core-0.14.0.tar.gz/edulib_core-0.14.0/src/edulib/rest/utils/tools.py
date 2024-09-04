import importlib
import pkgutil
from types import (
    ModuleType,
)

from django.db.models import (
    Case,
    CharField,
    Expression,
    Q,
    Value,
    When,
)
from django.db.models.functions import (
    Concat,
    Substr,
)


def import_submodules(package: str, module_name: str) -> list[ModuleType]:
    """Импортирует подмодули пакета."""
    package = importlib.import_module(package)
    modules = []

    for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
        if is_pkg:
            full_name = f'{package.__name__}.{name}'
            try:
                modules.append(importlib.import_module(module_name, full_name))
            except ModuleNotFoundError:
                continue

    return modules


def get_person_short_name(lookup: str = '') -> 'Expression':
    """
    Возвращает выражение для аннотации Инициалов одной строкой.
    """
    def f(attr):
        return '__'.join((lookup, attr)) if lookup else attr

    return Concat(
        f('surname'),
        Value(' '),
        Substr(f('firstname'), 1, 1),
        Value('.'),
        Case(
            When(
                ~Q(**{f('patronymic__exact'): ''}),
                then=Concat(
                    Substr(f('patronymic'), 1, 1),
                    Value('.')
                )
            ),
            default=Value('')
        ),
        output_field=CharField(),
    )
