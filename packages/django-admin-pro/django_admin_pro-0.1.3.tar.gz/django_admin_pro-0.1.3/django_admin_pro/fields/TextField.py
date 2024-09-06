from django_admin_pro.fields.Field import Field


class TextField(Field):
    def __init__(self, title: str, column: str | None = None) -> None:
        super().__init__(
            "text",
            title,
            column,
            {"template": "input", "extraAttributes": {"type": "text"}},
        )
