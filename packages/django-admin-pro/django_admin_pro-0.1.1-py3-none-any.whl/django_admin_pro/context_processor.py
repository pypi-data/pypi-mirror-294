from django.http import HttpRequest

from django_admin_pro.resource_manager import ResourceManager


def get_resource_manager(request: HttpRequest):
    resource_manager: ResourceManager = request.__getattribute__("resource_manager")

    return resource_manager.data
