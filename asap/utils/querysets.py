from django.db import models
from django.db.models import Case, Value, When


class AuthorableQuerySet(models.QuerySet):
    """
    QuerySet Mixin for models that use ``Authorable`` Mixin.
    """

    def authored_by(self, user):
        """
        Filter the QuerySet and return only the instances
        created by the user.
        :param user:
        :return:
        """
        return self.filter(author=user)

    def annotate_is_author(self, user):
        """
        Attach a `is_author` field, and set it to `True`
        if the user created the instance.

        :param user:
        """
        return self.annotate(is_author=Case(
            When(author=user, then=Value(True)),
            default=Value(False), output_field=models.BooleanField()
        ))
