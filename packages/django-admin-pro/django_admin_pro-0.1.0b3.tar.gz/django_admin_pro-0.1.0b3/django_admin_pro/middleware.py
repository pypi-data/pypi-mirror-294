from django.http import HttpRequest

from django_admin_pro.resource_manager import ResourceManager


class ResourceManagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        resource_manager = ResourceManager()

        resource_manager.load_resources(request=request)

        request.__setattr__("resource_manager", resource_manager)

        response = self.get_response(request)

        return response
