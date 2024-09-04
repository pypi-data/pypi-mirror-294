# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.lib_passport.documents.domain import (
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
        from edulib.core.lib_passport.documents.services import (
            handlers,
        )

        bus.add_command_handlers(
            (commands.CreateDocument, handlers.create_document),
            (commands.DeleteDocument, handlers.delete_document),
            (commands.UpdateDocument, handlers.update_document),
        )

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.lib_passport.documents.adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('documents', repository))
