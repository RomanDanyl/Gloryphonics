from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

from user.models import User


class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    Read permission for everyone, but write,
    update, or delete permissions only for the owner.
    """

    def has_object_permission(
        self, request: Request, view: object, obj: object
    ) -> bool:
        if request.method in SAFE_METHODS or request.user.is_staff:
            return True
        return obj.user == request.user


class IsManagerOrAdminOrReadOnly(BasePermission):
    """
    Read permission for everyone, but write,
    update, or delete permissions only for the owner.
    """

    def has_object_permission(
        self, request: Request, view: object, obj: object
    ) -> bool:
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            if request.user.is_staff or request.user.role in [
                User.RoleChoices.ADMIN,
                User.RoleChoices.MANAGER,
            ]:
                return True
            return obj.user == request.user
        else:
            return False
