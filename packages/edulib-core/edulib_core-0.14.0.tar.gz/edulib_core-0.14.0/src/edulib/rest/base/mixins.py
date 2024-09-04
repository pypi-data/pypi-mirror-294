from typing import (
    TYPE_CHECKING,
)

from explicit.django.domain.validation.exceptions import (
    handle_domain_validation_error,
)
from rest_framework import (
    status,
)
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import (
    Response,
)

from edulib.core import (
    bus,
)
from edulib.rest.base.decorators import (
    handle_django_validation_error,
)


if TYPE_CHECKING:
    from explicit.messagebus.commands import (
        Command,
    )


class CommandBasedCreateModelMixin(CreateModelMixin):
    """Миксин создания объекта с помощью команды."""

    create_command: type['Command']

    @handle_django_validation_error
    @handle_domain_validation_error
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = self.create_command(
            **serializer.validated_data | self.prepare_additional_create_command_data(request, *args, **kwargs)
        )
        result = bus.handle(command)

        return Response(data=self.get_serializer(result).data, status=status.HTTP_201_CREATED)

    def prepare_additional_create_command_data(self, request, *args, **kwargs):
        return {}


class CommandBasedUpdateModelMixin(UpdateModelMixin):
    """Миксин обновления объекта с помощью команды."""

    update_command: type['Command']

    @handle_django_validation_error
    @handle_domain_validation_error
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            partial=kwargs.pop('partial', False),
        )
        serializer.is_valid(raise_exception=True)

        command = self.update_command(id=kwargs.get(self.lookup_field), **serializer.validated_data)
        result = bus.handle(command)

        return Response(data=self.get_serializer(result).data, status=status.HTTP_200_OK)


class CommandBasedDestroyModelMixin(DestroyModelMixin):
    """Миксин удаления объекта с помощью команды."""

    delete_command: type['Command']

    @handle_django_validation_error
    @handle_domain_validation_error
    def destroy(self, request, *args, **kwargs):
        bus.handle(self.delete_command(id=kwargs.get(self.lookup_field)))

        return Response(status=status.HTTP_204_NO_CONTENT)
