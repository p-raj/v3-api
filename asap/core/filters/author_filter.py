from rest_framework.filters import BaseFilterBackend


class AuthorFilter(BaseFilterBackend):
    """
    Filter all the objects where
    the user is associated with the object.

    The filter ensures that a Object/Entity
    created by A is not visible to B
    """

    def filter_queryset(self, request, queryset, view):
        """
        The author should only be able to see only his objects.
        :return:
        """
        return queryset.filter(author=request.user)
