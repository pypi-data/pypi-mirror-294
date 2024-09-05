from inertia import render


def index(request):
    return render(request, "Event/Index", props={"events": "test"})
