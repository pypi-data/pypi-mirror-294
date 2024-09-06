from typing import Any

from django_admin_pro.fields.Field import Field


class FieldItem:
    def __init__(self, field: Field, value: Any) -> None:
        self.field = field
        self.value = value
