from rest_framework import exceptions, permissions


class IsAuthorOrAuthorized(permissions.IsAuthenticated):
    """
    Either the author has the access or
    the request carries additional information that implies
    the authorization has granted the permission.
    """

    def has_permission(self, request, view):
        # all the authenticated users have direct access to the view
        # we might not be able to check the Authorization here
        # but we can filter out requests that definitely don't qualify.
        # for instance we do need the Authorization header to check for
        # object level permission
        # if the client is neither authenticated nor it has Authorization header
        # give it a hard time :)
        has_permission = super(IsAuthorOrAuthorized, self).has_permission(request, view)
        return has_permission or bool(request.META.get('HTTP_AUTHORIZATION', None))

    def has_object_permission(self, request, view, obj):
        has_method = getattr(obj, 'has_permission', None)
        has_permission = has_method and has_method(
            request.META.get('HTTP_AUTHORIZATION', None)
        )

        if not has_permission:
            raise exceptions.PermissionDenied()
        return has_permission
