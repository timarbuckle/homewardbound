from django.urls import path

from . import views

urlpatterns = [
    path("", views.cat_list_view, name="cat_list"),
    path("update/", views.update_cats_view, name="update_cats"),
]