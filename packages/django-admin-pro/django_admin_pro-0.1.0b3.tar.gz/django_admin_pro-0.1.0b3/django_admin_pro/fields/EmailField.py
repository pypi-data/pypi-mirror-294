from django_admin_pro.fields.Field import Field


class EmailField(Field):
    def __init__(self, title: str, column: str | None = None) -> None:
        super().__init__(
            "email",
            title,
            column,
            {"template": "input", "extraAttributes": {"type": "email"}},
        )
