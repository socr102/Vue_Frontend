from rest_framework.exceptions import ValidationError

class QueryParamTrendsMixin:
    def read_query_params(self):
        direction = self.request.query_params.get('direction', None)
        try:
            limit = self.request.query_params.get('limit', None)
            if limit: limit = int(limit)
        except ValueError:
            raise ValidationError({"limit": "Integer value required"})

        return sort_by, limit