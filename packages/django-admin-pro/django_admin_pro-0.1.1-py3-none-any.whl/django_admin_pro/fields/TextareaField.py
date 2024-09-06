from django_admin_pro.fields.Field import Field
from typing import Self


class TextareaField(Field):
    def __init__(self, title: str, column: str | None = None) -> None:
        super().__init__(
            "textarea",
            title,
            column,
            {"template": "textarea", "extraAttributes": {"type": "textarea"}},
        )

    def rows(self, rows: int) -> Self:
        self.num_rows = rows
        return self

    def cols(self, cols: int) -> Self:
        self.num_cols = cols
        return self
