# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.lib_passport.cleanup_days.domain import (
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
        from edulib.core.lib_passport.cleanup_days.services import (
            handlers,
        )

        bus.add_command_handlers(
            (commands.CreateCleanupDay, handlers.create_cleanup_day),
            (commands.DeleteCleanupDay, handlers.delete_cleanup_day),
        )

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.lib_passport.cleanup_days.adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('cleanup_days', repository))
