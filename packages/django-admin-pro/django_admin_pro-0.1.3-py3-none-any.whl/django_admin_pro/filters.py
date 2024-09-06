from typing import Any, Dict

from abc import abstractmethod
from django.http import HttpRequest
from django.db.models.query import QuerySet


class Filter:
    def __init__(self) -> None:
        self.filter_name = self.__class__.__name__

    @abstractmethod
    def apply(self, request: HttpRequest, queryset: QuerySet, value: Any) -> QuerySet:
        raise NotImplemented

    @abstractmethod
    def options(self, request: HttpRequest) -> Dict[str, Any]:
        raise NotImplemented
