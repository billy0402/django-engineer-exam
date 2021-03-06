from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and \
               (request.user.is_staff or request.user.is_superuser)


class IsEmployeeOrManagerUser(BasePermission):
    """
    Allows access only to user role with employee or manager.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_employee
