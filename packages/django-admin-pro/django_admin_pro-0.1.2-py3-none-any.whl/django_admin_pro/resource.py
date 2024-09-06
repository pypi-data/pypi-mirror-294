import re
import unicodedata

from abc import abstractmethod, abstractproperty
from importlib import import_module
from django.db import models
from django.http import HttpRequest


class Resource:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.resource_name = self.__class__.__name__
        self.resource_plural_name = self.__resource_plural_name()
        self.resource_key = self.__get_resource_key()

    @property
    @abstractmethod
    def model(self) -> str:
        raise NotImplemented

    @abstractmethod
    def fields(self, request: HttpRequest):
        raise NotImplemented

    @abstractmethod
    def cards(self, request: HttpRequest):
        raise NotImplemented

    @abstractmethod
    def filters(self, request: HttpRequest):
        raise NotImplemented

    @abstractmethod
    def lenses(self, request: HttpRequest):
        raise NotImplemented

    @abstractmethod
    def actions(self, request: HttpRequest):
        raise NotImplemented

    def __resource_plural_name(self):
        name = re.sub(r"(?<!^)(?=[A-Z])", " ", self.resource_name)

        if name.endswith("y") and not name.endswith(("ay", "ey", "iy", "oy", "uy")):
            plural_name = re.sub(r"y$", "ies", name)
        elif name.endswith(("s", "x", "z", "ch", "sh")):
            plural_name = f"{name}es"
        else:
            plural_name = f"{name}s"

        return plural_name

    def __get_resource_key(self):
        normalized_string = (
            unicodedata.normalize("NFKD", self.resource_plural_name)
            .encode("ascii", "ignore")
            .decode("utf-8")
        )

        lowercased_string = normalized_string.lower()

        cleaned_string = re.sub(r"[^a-z0-9\s-]", "", lowercased_string)

        slug = re.sub(r"[\s-]+", "-", cleaned_string).strip("-")

        return slug

    def get_model(self) -> models.Model:
        array = self.model.split(".")

        last = array.pop()

        model = import_module(".".join(array))

        return getattr(model, last)

    def get_fields(self):
        return self.fields(self.request)

    def get_filters(self):
        return [
            {"filter": filter, "filter_options": filter.options(self.request)}
            for filter in self.filters(self.request)
        ]
