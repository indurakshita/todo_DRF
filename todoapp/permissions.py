from rest_framework import permissions

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user if obj else True

    def has_permission(self, request, view):
        return True


# class ReadOnlyOrAuthenticatedPermission(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS and not request.user.is_authenticated:
#             return True
#         elif request.user and request.user.is_authenticated:
#             return True
#         return False
