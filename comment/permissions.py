from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated
        )
    
class CommentPermissionClass(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            (request.user.is_authenticated and 
            request.user.is_staff and
            request.method == "DELETE") or
            (request.user.is_authenticated and obj.author == request.user)
        )