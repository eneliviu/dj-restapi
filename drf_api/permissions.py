from rest_framework import permissions

# Custom permissions:
# - Object-level to see if a user is the owner
#   - It has to be an object-level permission, which  means we’ll have to
#     check a Profile model instance object and see if its ‘owner’ field
#     is  pointing to the same user who’s making the request.
# - Allow read-only access to anyone
#     - using the so-called safe http  methods, like GET, return True.
# - allow only the owner to update the resource:
#     - If the user is making a PUT or PATCH request, return True only if that
#       user owns the profile object.


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
