from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import District, Location, Organizer

admin.site.site_header = "Organizer Directory Admin"
admin.site.site_title = "Organizer Directory"
admin.site.index_title = "Data Upload and Management"
admin.site.index_template = "admin/custom_index.html"


admin.site.unregister(User)


@admin.register(User)
class ReceptionUserAdmin(UserAdmin):
    list_display = ("username", "is_active", "is_staff", "is_superuser", "date_joined")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    actions = ("approve_reception_users",)

    @admin.action(description="Approve selected reception users")
    def approve_reception_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} user(s) approved.")


class OrganizerAdminForm(forms.ModelForm):
    bulk_locations = forms.CharField(
        label="Bulk locations",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Paste comma-separated locations, e.g. Area One, Area Two, Area Three",
            }
        ),
        help_text="Enter comma-separated location names. They will be created and linked to this organizer on save.",
    )

    class Meta:
        model = Organizer
        fields = "__all__"


class LocationInline(admin.TabularInline):
    model = Location
    extra = 0
    fields = ("name", "district", "aliases")
    ordering = ("name",)


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    form = OrganizerAdminForm
    fieldsets = (
        ("Organizer details", {
            "fields": ("name", "phone_number", "district"),
        }),
        ("Bulk location upload", {
            "fields": ("bulk_locations",),
            "description": "Paste all locations for this organizer in one comma-separated list, then save.",
        }),
    )
    list_display = ("name", "phone_number", "district", "location_count")
    list_filter = ("district",)
    list_display_links = ('name',)  # അഡ്മിൻ പാനലിൽ പേരിൽ ക്ലിക്ക് ചെയ്താൽ എഡിറ്റ് ചെയ്യാം
    search_fields = ("name", "phone_number", "district__name", "locations__name")
    inlines = [LocationInline]

    @admin.display(description="Locations")
    def location_count(self, obj):
        return obj.locations.count()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        bulk_locations = form.cleaned_data.get("bulk_locations", "")
        location_names = {
            name.strip()
            for name in bulk_locations.split(",")
            if name.strip()
        }

        for location_name in sorted(location_names):
            Location.objects.get_or_create(
                organizer=obj,
                name=location_name,
                defaults={"district": obj.district},
            )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "organizer", "district")
    list_filter = ("district", "organizer")
    search_fields = ("name", "aliases", "organizer__name", "organizer__phone_number", "district__name", "organizer__district__name")
    autocomplete_fields = ("organizer",)

    @admin.display(description="District", ordering="district__name")
    def district(self, obj):
        return obj.district.name if obj.district else obj.organizer.district.name