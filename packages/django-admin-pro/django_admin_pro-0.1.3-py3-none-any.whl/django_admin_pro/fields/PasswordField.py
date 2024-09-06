from django_admin_pro.fields.Field import Field


class PasswordField(Field):
    def __init__(self, title: str, column: str | None = None) -> None:
        super().__init__(
            "password",
            title,
            column,
            {"template": "input", "extraAttributes": {"type": "password"}},
        )
