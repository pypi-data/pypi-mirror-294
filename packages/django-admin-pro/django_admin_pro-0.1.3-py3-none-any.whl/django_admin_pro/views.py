from pathlib import Path
from typing import Any, Dict, List
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.views.decorators.http import require_http_methods

from django_admin_pro.field_item import FieldItem
from django_admin_pro.resource_manager import ResourceManager


def signin(request: HttpRequest):
    return redirect(settings.LOGIN_URL)


def signout(request: HttpRequest):
    logout(request=request)
    return redirect(settings.LOGIN_URL)


def home(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("dashboard/main")
    else:
        return redirect(settings.LOGIN_URL)


@login_required(login_url=settings.LOGIN_URL)
def dashboard(request: HttpRequest):
    root_path = Path(__file__).parent

    template_path = f"{root_path}/templates/dashboard.html"

    return render(request, template_path)


def map_field_items(item, fields):
    items = []

    for key, value in item.items():
        for field in fields:
            if key == field.column:
                items.append(FieldItem(field=field, value=value))

    return items


def apply_filters(
    request: HttpRequest, queryset: QuerySet, filters: List[Dict[str, Any]]
) -> QuerySet:
    loaded_filters = request.GET.get("filter")

    if not loaded_filters:
        return queryset.filter()

    filters_list = loaded_filters.split("__")

    for filter in filters:
        filter_instance = filter["filter"]

        if filter_instance.filter_name == filters_list[0]:
            queryset = filter_instance.apply(request, queryset, filters_list[1])

    return queryset


def test_function():
    print("test")


@login_required(login_url=settings.LOGIN_URL)
def list_resources(request: HttpRequest, resource_key: str):
    resource_manager: ResourceManager = request.__getattribute__("resource_manager")

    resource = resource_manager.get_resource(resource_key)

    model = resource.get_model()

    fields = resource.get_fields()

    filters = resource.get_filters()

    fields_keys = [field.column for field in fields]

    queryset = model.objects.get_queryset()

    queryset__results = (
        apply_filters(request, queryset, filters)
        .values(*fields_keys)
        .order_by("id")
        .all()
    )

    per_page = int(request.GET.get("per_page", 25))

    page = int(request.GET.get("page", 1))

    paginator = Paginator(queryset__results, per_page)

    page_obj = paginator.page(page)

    items = [map_field_items(item, fields) for item in page_obj]

    root_path = Path(__file__).parent

    template_path = f"{root_path}/templates/index.html"

    start_record = (page_obj.number - 1) * per_page + 1

    end_record = min(page_obj.number * per_page, paginator.count)

    query_params = request.GET.copy()

    if page_obj.has_next():
        query_params["page"] = str(page_obj.next_page_number())
        next_page_url = f"{request.path}?{query_params.urlencode()}"
    else:
        next_page_url = None

    if page_obj.has_previous():
        query_params["page"] = str(page_obj.previous_page_number())
        previous_page_url = f"{request.path}?{query_params.urlencode()}"
    else:
        previous_page_url = None

    return render(
        request,
        template_path,
        {
            "fields": fields,
            "filters": filters,
            "items": items,
            "resource": resource,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "start_record": start_record,
                "end_record": end_record,
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "previous_page_url": previous_page_url,
                "next_page_url": next_page_url,
            },
        },
    )


@login_required(login_url=settings.LOGIN_URL)
def resource_detail(request: HttpRequest, resource_key: str, resource_model_id: int):
    resource_manager: ResourceManager = request.__getattribute__("resource_manager")

    resource = resource_manager.get_resource(resource_key)

    model = resource.get_model()

    fields = resource.fields(request)

    fields_keys = [field.column for field in fields]

    queryset = model.objects.values(*fields_keys).filter(id=resource_model_id).first()

    items = map_field_items(queryset, fields)

    root_path = Path(__file__).parent

    template_path = f"{root_path}/templates/detail.html"

    return render(
        request,
        template_path,
        {"fields": fields, "items": items, "resource": resource},
    )


@login_required(login_url=settings.LOGIN_URL)
def new_resource(request: HttpRequest, resource_key: str):
    resource_manager: ResourceManager = request.__getattribute__("resource_manager")

    resource = resource_manager.get_resource(resource_key)

    fields = resource.fields(request)

    root_path = Path(__file__).parent

    template_path = f"{root_path}/templates/new.html"

    return render(
        request,
        template_path,
        {"fields": fields, "resource": resource},
    )


@require_http_methods(["POST"])
@login_required(login_url=settings.LOGIN_URL)
def create_new_resource(request: HttpRequest, resource_key: str):
    resource_manager: ResourceManager = request.__getattribute__("resource_manager")

    resource = resource_manager.get_resource(resource_key)

    fields = resource.fields(request)

    post_data = request.POST.dict()

    form_fields = [field.column for field in fields if "forms" in field.visibility]

    filtered_data = {
        key: value for key, value in post_data.items() if key in form_fields
    }

    model = resource.get_model()

    created_model = model.objects.create(**filtered_data)

    return redirect(
        "resource_detail",
        resource_key=resource.resource_key,
        resource_model_id=created_model.id,
    )
