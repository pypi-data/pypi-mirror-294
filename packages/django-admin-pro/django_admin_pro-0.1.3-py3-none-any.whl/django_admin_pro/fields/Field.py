import re

from typing import Any, Dict, Self


class Field:
    def __init__(
        self,
        type: str,
        title: str,
        column: str | None = None,
        meta: Dict[str, Any] = {},
    ) -> None:
        self.type = type
        self.title = title
        self.column = column if column else self.title_to_column_name(self.title)
        self.__meta = meta
        self.__visibility = ["index", "detail", "forms"]

    @property
    def meta(self) -> Dict[str, Any]:
        return self.__meta

    @property
    def visibility(self) -> Dict[str, Any]:
        return self.__visibility

    def withMeta(self, meta: Dict[str, Any]) -> Self:
        self.__meta = self.merge_dicts(meta, self.__meta)
        return self

    def onlyOnForms(self) -> Self:
        self.__visibility = ["forms"]
        return self

    def hideOnForms(self) -> Self:
        self.__visibility.remove("forms")
        return self

    def title_to_column_name(self, title: str) -> str:
        title = title.replace(" ", "_").lower()
        title = re.sub(r"(?<!^)(?=[A-Z])", "_", title).lower()
        return title

    def merge_dicts(self, dict1, dict2) -> Dict[str, Any]:
        merged = dict1.copy()

        for key, value in dict2.items():
            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                merged[key] = self.merge_dicts(merged[key], value)
            else:
                merged[key] = value

        return merged
