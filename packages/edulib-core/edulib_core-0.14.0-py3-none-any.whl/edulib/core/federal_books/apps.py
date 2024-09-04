# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.federal_books.domain import (
    commands,
)


class AppConfig(AppConfigBase):

    name = __package__

    def ready(self):
        self._register_commands()
        self._register_repositories()

    def _register_commands(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.federal_books.services import (
            handlers,
        )

        bus.add_command_handlers(
            (commands.CreateFederalBook, handlers.create_federal_book),
            (commands.UpdateFederalBook, handlers.update_federal_book),
        )

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.federal_books.adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('federal_books', repository))
