from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .district_resolver import resolve_district_name
from .forms import DataUploadForm, ManualOrganizerForm
from .importers import import_directory_file
from .models import District, Location, Organizer


def _is_dashboard_admin(user):
    return user.is_authenticated and user.is_staff


def admin_login(request):
    if _is_dashboard_admin(request.user):
        return redirect("custom_admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("custom_admin_dashboard")

        messages.error(request, "Invalid admin username or password.")

    return render(request, "dashboard/login.html")


def admin_logout(request):
    logout(request)
    return redirect("custom_admin_login")


@user_passes_test(_is_dashboard_admin, login_url="custom_admin_login")
def dashboard(request):
    context = {
        "district_count": District.objects.count(),
        "organizer_count": Organizer.objects.count(),
        "location_count": Location.objects.count(),
        "pending_users": User.objects.filter(is_active=False).count(),
        "recent_organizers": Organizer.objects.select_related("district").order_by("-id")[:6],
    }
    return render(request, "dashboard/index.html", context)


@user_passes_test(_is_dashboard_admin, login_url="custom_admin_login")
def data_upload(request):
    form = DataUploadForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        try:
            summary = import_directory_file(form.cleaned_data["upload_file"])
        except ValueError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(
                request,
                "Upload complete: "
                f"{summary['districts']} districts, "
                f"{summary['organizers']} organizers, "
                f"{summary['locations']} locations created. "
                f"{summary['skipped_rows']} rows skipped.",
            )
            form = DataUploadForm()

    return render(request, "dashboard/data_upload.html", {"form": form})


@user_passes_test(_is_dashboard_admin, login_url="custom_admin_login")
def manual_upload(request):
    form = ManualOrganizerForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        first_location = form.cleaned_data["locations"][0]
        district_name = resolve_district_name(first_location, form.cleaned_data["district"])
        district, _ = District.objects.get_or_create(name=district_name)
        organizer, _ = Organizer.objects.get_or_create(
            name=form.cleaned_data["organizer"].strip(),
            phone_number=form.cleaned_data["phone_number"].strip(),
            district=district,
        )

        created_locations = 0
        aliases = form.cleaned_data.get("aliases") or []
        for index, location_name in enumerate(form.cleaned_data["locations"]):
            location_district_name = resolve_district_name(
                location_name,
                form.cleaned_data["district"],
            )
            location_district, _ = District.objects.get_or_create(name=location_district_name)
            alias = aliases[index] if index < len(aliases) else ""
            _, created = Location.objects.get_or_create(
                name=location_name,
                organizer=organizer,
                defaults={"district": location_district, "aliases": alias},
            )
            created_locations += int(created)

        messages.success(request, f"Organizer saved with {created_locations} new location(s).")
        return redirect("custom_admin_manual_upload")

    return render(request, "dashboard/manual_upload.html", {"form": form})


@user_passes_test(_is_dashboard_admin, login_url="custom_admin_login")
def reception_users(request):
    if request.method == "POST":
        user_ids = request.POST.getlist("user_ids")
        updated = User.objects.filter(id__in=user_ids, is_staff=False).update(is_active=True)
        messages.success(request, f"{updated} reception user(s) approved.")
        return redirect("custom_admin_users")

    users = User.objects.filter(is_staff=False).order_by("is_active", "-date_joined")
    return render(request, "dashboard/users.html", {"users": users})
