# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.lib_registry import (
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
            exchange_fund,
            info_product_marks,
            registry_entries,
            registry_examples,
        )

        bus.get_uow().register_repositories(
            ('exchange_fund', exchange_fund),
            ('registry_entries', registry_entries),
            ('registry_examples', registry_examples),
            ('info_product_marks', info_product_marks),
        )

    def _register_commands(self) -> None:
        from edulib.core import (
            bus,
        )
        from edulib.core.lib_registry import (
            services,
        )

        bus.add_command_handlers(
            (domain.CreateRegistryEntry, services.create_registry_entry),
            (domain.UpdateRegistryEntry, services.update_registry_entry),
            (domain.DeleteRegistryEntry, services.delete_registry_entry),
            (domain.CreateRegistryExample, services.create_registry_example),
            (domain.UpdateRegistryExample, services.update_registry_example),
            (domain.DeleteRegistryExample, services.delete_registry_example),
            (domain.CopyRegistryExample, services.copy_registry_example),
        )
