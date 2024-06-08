from functools import reduce
from operator import or_
from typing import Type, List
from django.db import models
from rest_framework import filters
from rest_framework.request import Request
from rest_framework.views import APIView
from admin_auto_filters.filters import AutocompleteFilter


def CustomFilter(
    *, query_param: str, query_field: str
) -> Type[filters.BaseFilterBackend]:
    """
    Create a custom filter class for exact matches on a single field.
    Args:
        query_param (str): The query parameter to filter by.
        query_field (str): The model field to filter on.
    Returns:
        Type[filters.BaseFilterBackend]: A class that performs the filtering.
    """

    class FilterClass(filters.BaseFilterBackend):
        def filter_queryset(
            self, request: Request, queryset: models.QuerySet, view: APIView
        ) -> models.QuerySet:
            """
            Filter the queryset based on the query parameter value.
            Args:
                request (Request): The HTTP request object.
                queryset (models.QuerySet): The queryset to filter.
                view (APIView): The view instance.
            Returns:
                models.QuerySet: The filtered queryset.
            """
            query_value = request.query_params.get(query_param)
            if query_value:
                return queryset.filter(**{f"{query_field}__iexact": query_value})
            return queryset

    return FilterClass


def CustomSearch(
    *, query_param: str, query_fields: List[str]
) -> Type[filters.BaseFilterBackend]:
    """
    Create a custom search class for partial matches on multiple fields.
    Args:
        query_param (str): The query parameter to search by.
        query_fields (List[str]): The model fields to search on.
    Returns:
        Type[filters.BaseFilterBackend]: A class that performs the searching.
    """

    class SearchClass(filters.BaseFilterBackend):
        def filter_queryset(
            self, request: Request, queryset: models.QuerySet, view: APIView
        ) -> models.QuerySet:
            """
            Filter the queryset based on the query parameter value.
            Args:
                request (Request): The HTTP request object.
                queryset (models.QuerySet): The queryset to filter.
                view (APIView): The view instance.
            Returns:
                models.QuerySet: The filtered queryset.
            """
            query_value = request.query_params.get(query_param)
            if query_value:
                return queryset.filter(
                    reduce(
                        or_,
                        (
                            models.Q(**{f"{field}__icontains": query_value})
                            for field in query_fields
                        ),
                    )
                )
            return queryset

    return SearchClass


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
