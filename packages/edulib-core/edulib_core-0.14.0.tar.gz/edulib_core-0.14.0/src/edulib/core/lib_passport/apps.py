# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.lib_passport.domain import (
    commands,
)


class AppConfig(AppConfigBase):

    name = __package__

    def ready(self):
        self._register_commands()
        self._register_event_handlers()
        self._register_repositories()

    def _register_commands(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.lib_passport.services import (
            handlers,
        )

        bus.add_command_handlers(
            (commands.CreatePassport, handlers.create_passport),
            (commands.CreateWorkMode, handlers.create_work_mode),
            (commands.DeletePassport, handlers.delete_passport),
            (commands.DeleteWorkMode, handlers.delete_work_mode),
            (commands.UpdatePassport, handlers.update_passport),
            (commands.UpdateWorkMode, handlers.update_work_mode),
        )

    def _register_event_handlers(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.schools import (
            domain as schools,
        )

        from . import (
            services,
        )

        for event, handler in (
            (schools.SchoolProjectionCreated, services.on_school_projection_created),
            (schools.SchoolProjectionUpdated, services.on_school_projection_updated)
        ):
            bus.add_event_handler(event, handler)

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.lib_passport.adapters.db import (
            passport_repository,
            work_mode_repository,
        )

        bus.get_uow().register_repositories(('passports', passport_repository), ('work_modes', work_mode_repository))
