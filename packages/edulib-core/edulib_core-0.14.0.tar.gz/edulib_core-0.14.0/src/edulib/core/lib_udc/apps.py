# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.lib_udc import (
    domain,
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
        from edulib.core.lib_udc import (
            services,
        )

        bus.add_command_handlers(
            (domain.CreateUdc, services.create_udc),
            (domain.UpdateUdc, services.update_udc),
            (domain.DeleteUdc, services.delete_udc),
        )

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.lib_udc.adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('udc', repository))
