from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import ADMIN, USER, MODERATOR


class IsAdminOrMod(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                (request.method in SAFE_METHODS)
                or request.user.is_superuser
                or (request.user.role in [USER, ADMIN, MODERATOR])
            )
        else:
            return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.is_superuser
                or (request.user.role in [ADMIN, MODERATOR])
                or obj.author == request.user
            )
        else:
            return request.method in SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == ADMIN
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.role == ADMIN
            or request.method in SAFE_METHODS
        )


class AdminOnly(BasePermission):
    actions = ['retrieve', 'update', 'partial_update', 'destroy']

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == ADMIN
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == ADMIN or view.action in self.actions
        )


class OwnerOnly(BasePermission):

    actions = ['retrieve', 'update', 'partial_update']

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj.username == request.user
            and view.action in self.actions
        )
