from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied


class DocAccessMixin(AccessMixin):
    permission_denied_message = 'You are not authorized to view this content.'

    def handle_no_permission(self):
        if self.raise_exception:
            messages.error(self.request, self.permission_denied_message)
            raise PermissionDenied(self.get_permission_denied_message())
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class SuperUserAccessMixin(AccessMixin):
    permission_denied_message = 'You are not authorized to view this content.'

    def handle_no_permission(self):
        if self.raise_exception:
            messages.error(self.request, self.permission_denied_message)
            raise PermissionDenied(self.get_permission_denied_message())
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)