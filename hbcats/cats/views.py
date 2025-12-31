from datetime import time, timedelta

from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Cat, CatStatus


# Create your views here.
def cat_list_view(request):
    filter_type = request.GET.get("filter", "all")
    cats = Cat.objects.none()

    if request.headers.get("HX-Request"):
        if filter_type == "new":
            cats = Cat.objects.filter(status=CatStatus.NEW)
        elif filter_type == "adopted":
            time_threshold = timezone.now() - timedelta(hours=24)
            cats = Cat.objects.filter(status=CatStatus.ADOPTED, last_seen__gte=time_threshold)
        else:
            cats = Cat.objects.filter(Q(status=CatStatus.AVAILABLE) | Q(status=CatStatus.NEW))

        context = {"cats": cats}
        return render(request, "cats/cat_table.html", context)

    context = {"cats": cats}
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

    return render(request, "cats")


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
