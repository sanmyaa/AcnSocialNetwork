from functools import reduce
from operator import or_
from typing import List, Type

from admin_auto_filters.filters import AutocompleteFilter
from django.db import models
from rest_framework import filters
from rest_framework.request import Request
from rest_framework.views import APIView


def CustomFilterSearch(
    *, query_param: str, search_fields: List[str], filter_fields: List[str]
) -> Type[filters.BaseFilterBackend]:

    class FilterClass(filters.BaseFilterBackend):
        def filter_queryset(
            self, request: Request, queryset: models.QuerySet, view: APIView
        ) -> models.QuerySet:

            query_value = request.query_params.get(query_param)
            if query_value:
                filtered_queryset = queryset.filter(
                    reduce(
                        or_,
                        (
                            models.Q(**{f"{f_field}__iexact": query_value})
                            for f_field in filter_fields
                        ),
                    )
                )
                if filtered_queryset.exists():
                    return filtered_queryset

                searched_queryset = queryset.filter(
                    reduce(
                        or_,
                        (
                            models.Q(**{f"{f_field}__icontains": query_value})
                            for f_field in search_fields
                        ),
                    )
                )
                if searched_queryset.exists():
                    return searched_queryset

                return queryset.none()

            return queryset

    return FilterClass


def admin_list_filter(title, field_name) -> Type[AutocompleteFilter]:
    """
    Create an admin list filter with autocomplete functionality.
    Args:
        title (str): The title of the filter to display in the interface.
        field_name (str): The model field name to filter on.
    Returns:
        Type[AutocompleteFilter]: Searchable dropdown filter.
    """
    return type(
        "AdmiListFilter",
        (AutocompleteFilter,),
        {"title": title, "field_name": field_name},
    )
