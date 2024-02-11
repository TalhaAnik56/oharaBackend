from rest_framework.permissions import BasePermission, IsAdminUser


class IsAdminOrIsSeller(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff or hasattr(request.user, "seller"))
