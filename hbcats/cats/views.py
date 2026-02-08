import logging
from datetime import timedelta

from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET  #, require_http_methods
from django.http import HttpResponse, JsonResponse

from .models import Cat, CatStatus

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)


def cat_list_view(request):
    filter_type = request.GET.get("filter", "all")
    sort = request.GET.get("sort", "name")  # Default sorting by name
    sort_order = request.GET.get("sort_order", "asc")  # Default to ascending order
    valid_statuses = [CatStatus.AVAILABLE, CatStatus.NEW]

    valid_sort_fields = [
        "name",
        "status",
        "age",
        "intake_date",
        "sex",
        "breed",
        "primary_color",
        "location",
    ]
    logger.info(f"cat_list_view filter_type: {filter_type}, sort: {sort}, sort_order: {sort_order}")

    # Ensure the sort field is valid
    if sort not in valid_sort_fields:
        sort = "name"

    # Handle age sorting explicitly
    sort_field = sort
    if sort == "age":
        if sort_order == "desc":
            sort_field = "-birthday"  # Oldest first for descending age
        else:
            sort_field = "birthday"  # Youngest first for ascending age
    else:
        # Determine the sorting direction for other fields
        if sort_order == "desc":
            sort_field = f"-{sort}"

    # Filter the cats based on the filter_type
    if filter_type == "new":
        time_threshold = timezone.now() - timedelta(hours=24)
        cats = Cat.objects.filter(
            Q(status=CatStatus.AVAILABLE) | Q(status=CatStatus.NEW),
            first_seen__gte=time_threshold,
        )
    elif filter_type == "adopted":
        cats = Cat.objects.recent().filter(status=CatStatus.ADOPTED)
    elif filter_type == "none":
        cats = Cat.objects.all()
    else:
        cats = Cat.objects.filter(
            Q(status=CatStatus.AVAILABLE) | Q(status=CatStatus.NEW)
        )

    context = {
        "cats": cats.order_by(sort_field),
        "current_filter": filter_type,
        "current_sort": sort,
        "current_sort_order": "desc"
        if sort_field.startswith("-")
        else "asc",  # Toggle sort order
        "total_cats": Cat.objects.filter(status__in=valid_statuses).count(),
        "new_cats": Cat.objects.filter(status=CatStatus.NEW).count(),
        "adopted_cats": Cat.objects.recent().filter(status=CatStatus.ADOPTED).count(),
    }

    # Render the appropriate template
    if request.headers.get("HX-Request"):
        response = render(request, "cats/cat_table.html", context)
        response["HX-Trigger"] = "refreshStats"
        return response

    return render(request, "cats/dashboard.html", context)


# POST is used within the app from the menu via HTMX
# GET is used to run update without having to return
# a separate instance of the app via manage.py update
@require_POST
def update_cats_view(request):
    context = update_cats_latest()
    return render(request, "cats/stats_bar.html", context)

@require_GET
def update_cats_api_view(request):
    context = update_cats_latest()
    return JsonResponse(context)

def update_cats_latest():
    logger.info("calling update_cats")
    from .updatecats import UpdateCats
    updater = UpdateCats()
    response = updater.update_cats()
    logger.info("completed update_cats")

    context = {
        "total_cats": response["Total"],
        "new_cats": response["New"],
        "adopted_cats": response["Adopted"],
    }
    return context

@require_POST
def update_all_cats_view(request):
    update_all_cats_latest_details()
    cats = Cat.objects.filter(Q(status=CatStatus.AVAILABLE) | Q(status=CatStatus.NEW))

    context = {
        "cats": cats.order_by("name"),
        "current_filter": "all",
        "current_sort": "name",
        "current_sort_order": "asc",
    }
    return render(request, "cats/cat_table.html", context=context)

@require_GET
def update_all_cats_api_view(request):
    update_all_cats_latest_details()
    return HttpResponse(status=204)

def update_all_cats_latest_details():
    # update every cat's details, should be used rarely
    from .updatecats import UpdateCats

    logger.info("calling update_all_cat_details")
    updater = UpdateCats()
    updater.update_all_cat_details()
    logger.info("completed update_all_cat_details")
    return

@require_POST
def update_stats_view(request):
    valid_statuses = [CatStatus.AVAILABLE, CatStatus.NEW]

    context = {
        "total_cats": Cat.objects.filter(status__in=valid_statuses).count(),
        "new_cats": Cat.objects.filter(status=CatStatus.NEW).count(),
        "adopted_cats": Cat.objects.recent().filter(status=CatStatus.ADOPTED).count(),
    }
    return render(request, "cats/stats_bar.html", context)


def report_view(request):
    cats = Cat.objects.filter(
        Q(status=CatStatus.AVAILABLE) |
        Q(status=CatStatus.NEW)
        ).order_by("-birthday", "name")
    context = {
        "cats": cats,
    }
    return render(request, "cats/report.html", context)


@require_GET
def hello_world_api_view(request):
    return JsonResponse({"message": "Hello, World!"})
