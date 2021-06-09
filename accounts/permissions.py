from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = "You do not own this profile."

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return request.user.id == obj.user_id

class IsReviewerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow reviewer to edit their own review.
    """
    message = "You do not have access to this review."

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return request.user.id == obj.student_profile.user_id

class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow reviewer to edit their own comment.
    """
    message = "You do not have access to this comment."

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return request.user.id == obj.user_commenting.id

class IsVideoOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow reviewer to edit their own review.
    """
    message = "You do not have access to this review."

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return request.user.id == obj.creator_profile.user_id