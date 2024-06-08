from typing import Type

from rest_framework.pagination import PageNumberPagination


def make_paginator(
    page_size: int = 50, page_size_query_param: str = "page_size"
) -> Type[PageNumberPagination]:
    """
    Create a custom page-size and page-number based paginator.
    Args:
        page_size (int, optional): The default number of items per page.
        page_size_query_param (str, optional): The query param name for page size.
    Returns:
        Type[PageNumberPagination]: The custom paginator class.
    """
    return type(
        "CustomPaginator",
        (PageNumberPagination,),
        {"page_size": page_size, "page_size_query_param": page_size_query_param},
    )
