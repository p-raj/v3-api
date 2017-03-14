from rest_framework import permissions


class IsAuthorOrAuthorized(permissions.IsAuthenticated):
    """
    Either the author has the access or
    the request carries additional information that implies
    the authorization has granted the permission.
    """

    def has_permission(self, request, view):
        # TODO:
        # currently all the authentic users are authorized :/
        return super(IsAuthorOrAuthorized, self).has_permission(request, view)
