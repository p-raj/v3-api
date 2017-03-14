from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    All the authors have the full access
    to the objects created by them.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the author is same the authenticated user.

        :param request:
        :param view:
        :param obj:
        :return:
        """
        assert hasattr(obj, 'author'), 'AttributeError: obj has no attribute author'
        return (request.method in permissions.SAFE_METHODS or
                request.user == obj.author)
