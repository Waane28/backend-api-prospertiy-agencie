from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_system_admin

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer

class IsAdminOrSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and 
            (request.user.is_admin or request.user.is_system_admin)
        )
        
class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow customers to edit their own profile, admins to edit any."""
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner or an admin
        return obj == request.user or request.user.is_admin or request.user.is_system_admin