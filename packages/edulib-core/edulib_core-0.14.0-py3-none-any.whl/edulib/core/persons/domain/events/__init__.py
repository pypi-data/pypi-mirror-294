from .addresses import (
    AddressCreated,
    AddressDeleted,
    AddressUpdated,
)
from .documents import (
    PersonDocumentCreated,
    PersonDocumentDeleted,
    PersonDocumentUpdated,
)
from .persons import (
    PersonCreated,
    PersonDeleted,
    PersonUpdated,
)


__all__ = [
    'PersonCreated',
    'PersonUpdated',
    'PersonDeleted',
    'PersonDocumentCreated',
    'PersonDocumentUpdated',
    'PersonDocumentDeleted',
    'AddressCreated',
    'AddressDeleted',
    'AddressUpdated',
]
