# from tabnanny import verbose
# from typing_extensions import ReadOnly
from cats.updatecats import UpdateCats
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import messages
from django.urls import path
from django.shortcuts import redirect
# from django.db.models import Count

# Register your models here.
from .models import Cat
from datetime import date, time, datetime, timedelta


class RecentCatsFilter(admin.SimpleListFilter):
    title = "Recent Date"
    parameter_name = "recent_date"

    def lookups(self, request, model_admin):
        return [
            ("0days", "New Cats"),
            ("1days", "Adopted Cats"),
        ]

    def queryset(self, request, queryset):
        # today = date.today()
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)
        start_datetime = timezone.make_aware(
            timezone.datetime.combine(yesterday, time.min)
        )
        end_datetime = timezone.make_aware(timezone.datetime.combine(today, time.min))
        if self.value() == "0days":
            return queryset.filter(first_seen__gte=today)
        if self.value() == "1days":
            return queryset.filter(
                last_seen__gte=start_datetime, last_seen__lte=end_datetime
            )
            # return queryset.filter(
            #    last_seen__lte=datetime.combine(datetime.today(), time.min)
            # )


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
        "first_seen",
        "last_seen",
    )
    search_fields = ("name", "image_cy", "first_seen", "last_seen")
    list_filter = (RecentCatsFilter, "name", "last_seen")
    # readonly_fields = ("image_cy", "name", "image_url", "first_seen", "last_seen")

    # Define the custom method to display the image
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
    def large_photo_preview(self, obj):
        if obj.image_url:
            # Set larger dimensions (e.g., 200x200 or more)
            return format_html(
                '<img src="{}" width="200" height="200" style="border-radius: 5px; border: 1px solid #ccc;" />',
                obj.image_url,
            )
        return "No Image Uploaded"

    # Optional: Set a user-friendly column header
    photo_preview.short_description = "Photo"
    large_photo_preview.short_description = "Photo"

    # Optional: Allow the column header to be sorted by the photo field
    photo_preview.admin_order_field = "photo"
    large_photo_preview.admin_order_field = "photo"

    def pretty_name(self, obj):
        name = obj.name

        # Determine the color based on the price (optional enhancement)
        # Use format_html to securely inject the HTML and CSS
        # style="font-size: 1.2em; font-weight: bold; color: green;"
        return format_html(
            '<span style="font-size: 1.8em; font-weight: normal; color: {};">{}</span>',
            "black",
            name,
        )

    # Set a user-friendly column header
    pretty_name.short_description = "Price"

    # Allow sorting on the actual database field
    pretty_name.admin_order_field = "price"

    def total_cats(self, obj):
        return obj.cats.count()

    # Set a user-friendly column header
    total_cats.short_description = "Total Cats"

    # Allow sorting on the actual database field
    total_cats.admin_order_field = "cats"

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


admin.site.register(Cat, CatAdmin)
