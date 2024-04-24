from rest_framework.permissions import BasePermission


# class IsStaffUser(BasePermission):

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_staff


class IsOwnerProfile(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the profile
        return request.user.is_authenticated and obj == request.user