import glob
import os

from importlib import import_module
from django.http import HttpRequest
from django_admin_pro.resource import Resource


class ResourceManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(ResourceManager, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self) -> None:
        self.resources = {}
        self.folder_name = "genie"
        self.module_names = self.get_module_names()

    def get_module_names(self):
        folder_path = f"{self.folder_name}/resources"

        module_paths = glob.glob(os.path.join(folder_path, "*.py"), recursive=True)

        module_names = []

        for module_path in module_paths:
            module_name = os.path.splitext(os.path.relpath(module_path, folder_path))[0]

            if module_name != "__init__":
                module_names.append(module_name)

        return module_names

    def load_resources(self, request: HttpRequest):
        for module_name in self.module_names:
            resource_instance = self.__get_resource_instance(
                self.folder_name, module_name, request
            )

            self.resources[resource_instance.resource_key] = resource_instance

    def __get_resource_instance(
        self, folder_name: str, module_name: str, request: HttpRequest
    ) -> Resource:
        module = import_module(f"{folder_name}.resources.{module_name}")

        resource_class = getattr(module, module_name)

        return resource_class(request)

    def get_resource(self, resource_key: str) -> Resource:
        try:
            return self.resources[resource_key]
        except:
            raise Exception("error")

    @property
    def data(self):
        return {
            "resources": self.resources,
            "resources_list": [resource for resource in self.resources.values()],
        }
