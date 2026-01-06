import logging
from datetime import time, timedelta

# from imaplib import Commands
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Cat, CatStatus

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Create your views here.
def cat_list_view(request):
    filter_type = request.GET.get("filter", "all")
    sort = request.GET.get("sort", "name")  # Default sorting by name
    sort_order = request.GET.get("sort_order", "asc")  # Default to ascending order

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
    # logger.info(f"sort: {sort}, sort_order: {sort_order}")

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
        # logger.debug("Filtering new cats")
        time_threshold = timezone.now() - timedelta(hours=24)
        # cats = Cat.objects.filter(status=CatStatus.NEW)
        cats = Cat.objects.filter(
            Q(status=CatStatus.AVAILABLE) | Q(status=CatStatus.NEW),
            first_seen__gte=time_threshold,
        )
    elif filter_type == "adopted":
        # logger.debug("Filtering adopted cats seen in last 24 hours")
        time_threshold = timezone.now() - timedelta(hours=24)
        cats = Cat.objects.filter(
            status=CatStatus.ADOPTED, last_seen__gte=time_threshold
        )
        # cats = Cat.objects.filter(status=CatStatus.ADOPTED)
    else:
        # logger.debug("Filtering available cats")
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
    }

    # Render the appropriate template
    if request.headers.get("HX-Request"):
        return render(request, "cats/cat_table.html", context)

    return render(request, "cats/dashboard.html", context)


@require_POST
def update_cats_view(request):
    # This view would trigger the UpdateCats process
    from .updatecats import UpdateCats

    updater = UpdateCats()
    response = updater.update_cats()

    # After updating, redirect back to the cat list view
    # return redirect('cat_list')
    context = {
        "total_cats": response["Total"],
        "new_cats": response["New"],
        "adopted_cats": response["Adopted"],
    }

    # 3. RETURN ONLY THE STATS PARTIAL
    return render(request, "cats/stats_bar.html", context)


@require_POST
def update_all_cats_view(request):
    # This view would trigger the UpdateCats process
    from .updatecats import UpdateCats

    updater = UpdateCats()
    updater.update_all_cat_details()

    cats = Cat.objects.filter(Q(status=CatStatus.AVAILABLE) | Q(status=CatStatus.NEW))

    context = {
        "cats": cats.order_by("name"),
        "current_filter": "all",
        "current_sort": "name",
        "current_sort_order": "asc",
    }
    # return render(request, "cats/cat_table.html", {"cats": Cat.objects.all()})
    return render(request, "cats/cat_table.html", context=context)


@require_POST
def update_stats_view(request):
    from .models import Cat, CatStatus

    # valid_statuses = [CatStatus.AVAILABLE, CatStatus.NEW, CatStatus.ADOPTED]
    valid_statuses = [CatStatus.AVAILABLE, CatStatus.NEW]

    today = timezone.localdate()
    yesterday = today - timedelta(days=1)
    start_datetime = timezone.make_aware(timezone.datetime.combine(yesterday, time.min))

    context = {
        "total_cats": Cat.objects.filter(status__in=valid_statuses).count(),
        "new_cats": Cat.objects.filter(status=CatStatus.NEW).count(),
        "adopted_cats": Cat.objects.filter(
            status=CatStatus.ADOPTED, last_updated__gte=start_datetime
        ).count(),
    }
    return render(request, "cats/stats_bar.html", context)


def report_view(request):
    from .models import Cat  # , CatStatus

    cats = Cat.objects.filter(
        Q(status=CatStatus.AVAILABLE) |
        Q(status=CatStatus.NEW)
        ).order_by("-birthday", "name")
    context = {
        "cats": cats,
    }
    return render(request, "cats/report.html", context)
