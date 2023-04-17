"""Permissions."""

from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """Set permissions."""

    def has_permission(self, request, view):
        """List permissions."""
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Object permissions."""
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)
