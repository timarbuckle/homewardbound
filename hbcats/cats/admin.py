from datetime import time, timedelta

from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path
from django.utils import timezone
from django.utils.html import format_html

from cats.updatecats import UpdateCats

from .models import Cat, CatStatus, UpdateLog


class RecentCatsFilter(admin.SimpleListFilter):
    title = "Recent Date"
    parameter_name = "recent_date"

    def lookups(self, request, model_admin):
        return [
            ("0days", "New Cats"),
            ("1days", "Recently Adopted Cats"),
        ]

    def queryset(self, request, queryset):
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)
        start_datetime = timezone.make_aware(
            timezone.datetime.combine(yesterday, time.min)
        )
        # end_datetime = timezone.make_aware(timezone.datetime.combine(today, time.min))
        if self.value() == "0days":
            # return queryset.filter(first_seen__gte=today)
            return queryset.filter(status=CatStatus.NEW)
        if self.value() == "1days":
            return queryset.filter(
                status=CatStatus.ADOPTED, last_updated__gte=start_datetime
            )


class CatAdmin(admin.ModelAdmin):
    class Meta:
        model = Cat
        fields = "__all__"
        verbose_name = "Cats"
        verbose_name_plural = "Cats"
        ordering = ["last_seen", "name"]

    list_display = (
        "image_cy",
        "pretty_name",
        "large_photo_preview",
        "status",
        "breed",
        "location",
        "sex",
        "primary_color",
        "birthday",
        "intake_date",
        "first_seen",
        "last_seen",
    )
    search_fields = ("name", "image_cy", "first_seen", "last_seen")
    list_filter = (RecentCatsFilter, "last_seen", "name")
    # readonly_fields = ("image_cy", "name", "image_url", "first_seen", "last_seen")

    # Define the custom method to display the image
    @admin.display(description="Photo")
    def photo_preview(self, obj):
        # Check if the object has a photo file associated with it
        if obj.image_url:
            # Use format_html to securely render the HTML <img> tag
            # We set a max width/height for a nice thumbnail size
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px;" />',
                obj.image_url,
            )

        return "No Image"  # Return a string if no photo exists

    # Define the custom method for the large image display
    @admin.display(description="Photo")
    def large_photo_preview(self, obj):
        if obj.image_url:
            # Set larger dimensions (e.g., 200x200 or more)
            return format_html(
                '<img src="{}" width="200" height="200" style="border-radius: 5px; border: 1px solid #ccc;" />',
                obj.image_url,
            )
        return "No Image Uploaded"

    @admin.display(description="Name")
    def pretty_name(self, obj):
        name = obj.name

        return format_html(
            "<span style=\"font-family: 'ui-monospace', 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, 'DejaVu Sans Mono', monospace; font-weight: bold; font-size: 1.1em; color: {};\">{}</span>",
            "black",
            name,
        )

    @admin.display(description="Total Cats", ordering="cats")
    def total_cats(self, obj):
        return obj.cats.count()

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            cl = response.context_data["cl"]
            total_displayed_count = cl.queryset.count()

            if response.context_data is None:
                response.context_data = {}

            response.context_data["total_displayed_count"] = total_displayed_count

        except Exception as e:
            # Handle cases where context_data or cl might not be accessible
            print(f"Error calculating total count: {e}")
            pass

        return response
        # extra_context = extra_context or {}
        # extra_context["title"] = "Cats List"
        # return super().changelist_view(request, extra_context)

    def run_custom_task(self, request):
        # Implement your update logic here
        UpdateCats().update_cats()
        self.message_user(
            request, "Cat list updated successfully", level=messages.SUCCESS
        )

        # 3. Redirect back to the change list view
        return redirect("..")  # Redirects to the current admin list page

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "run-task/",  # The URL path for the button to link to
                self.admin_site.admin_view(self.run_custom_task),
                name="update cats",  # Name the URL for linking in the template
            ),
        ]
        return custom_urls + urls


class UpdateLogAdmin(admin.ModelAdmin):
    list_display = (
        "last_updated",
        "total_cats",
        "new_cats",
    )


admin.site.register(Cat, CatAdmin)
admin.site.register(UpdateLog, UpdateLogAdmin)
