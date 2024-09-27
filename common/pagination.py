from collections import OrderedDict
from typing import Any

from rest_framework import pagination
from rest_framework.response import Response


class TablePageNumberPagination(pagination.PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 250

    def get_paginated_response(self, data: Any) -> Response:
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("num_pages", self.page.paginator.num_pages),
                    ("page", self.page.number),
                    ("page_size", self.page.paginator.per_page),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ],
            ),
        )
