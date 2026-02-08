from django.urls import path

from . import views

urlpatterns = [
    path("", views.cat_list_view, name="cat_list"),
    path("update/", views.update_cats_view, name="update_cats"),
    path("update_all/", views.update_all_cats_view, name="update_all_cats"),
    path("api/update/", views.update_cats_api_view, name="update_cats_api"),
    path("api/update_all/", views.update_all_cats_api_view, name="update_all_cats_api"),
    path("api/hello/", views.hello_world_api_view, name="hello_world_api"),
    path("stats/", views.update_stats_view, name="update_stats"),
    path("report/", views.report_view, name="report"),
]
