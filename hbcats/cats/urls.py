from django.urls import path

from . import views

urlpatterns = [
    path("", views.cat_list_view, name="cat_list"),
    path("update/", views.update_cats_view, name="update_cats"),
    path("update_all/", views.update_all_cats_view, name="update_all_cats"),
    path("stats/", views.update_stats_view, name="update_stats"),
    path("report/", views.report_view, name="report"),
]
