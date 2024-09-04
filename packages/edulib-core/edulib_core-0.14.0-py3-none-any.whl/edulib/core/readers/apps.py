# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.readers import (
    domain,
)


class AppConfig(AppConfigBase):
    name = __package__

    def ready(self):
        self._register_repositories()
        self._register_commands()

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )

        from .adapters.db import (
            readers,
        )

        bus.get_uow().register_repositories(
            ('readers', readers),
        )

    def _register_commands(self) -> None:
        from edulib.core import (
            bus,
        )
        from edulib.core.readers import (
            services,
        )

        bus.add_command_handlers(
            (domain.UpdateReader, services.update_reader),
        )
