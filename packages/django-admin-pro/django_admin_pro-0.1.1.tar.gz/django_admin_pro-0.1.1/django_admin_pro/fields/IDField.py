from django_admin_pro.fields.Field import Field


class IDField(Field):
    def __init__(self, title: str, column: str | None = None) -> None:
        super().__init__("id", title, column)

        self.hideOnForms()
