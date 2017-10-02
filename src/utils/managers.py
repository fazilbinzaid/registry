from django.db import models

# rest_framework


# custom imports


class RoleQuerySet(models.QuerySet):
    """
    Custom QuerySet as manager provides filtering by GET parameters.
    """

    def filter_by_query_params(self, request):
        """
        Provides filtering by GET parameters.
        """
        items = self
        code_str = request.GET.get('code')

        if code_str:
            items = items.filter(code=code_str.strip().upper())

        return items
