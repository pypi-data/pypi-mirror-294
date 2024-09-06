from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("dashboard/main", views.dashboard, name="dashboard"),
    path("resources/<str:resource_key>", views.list_resources, name="list_resources"),
    path(
        "resources/<str:resource_key>/<int:resource_model_id>",
        views.resource_detail,
        name="resource_detail",
    ),
    path("resources/<str:resource_key>/new", views.new_resource, name="new_resource"),
    path(
        "resources/<str:resource_key>/new/create",
        views.create_new_resource,
        name="create_new_resource",
    ),
]
