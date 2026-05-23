from difflib import SequenceMatcher, get_close_matches

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from .forms import ReceptionRegistrationForm
from .language_search import search_terms
from .models import District, Location, Organizer


def reception_login(request):
    if request.user.is_authenticated:
        return redirect("directory:home")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)
            return redirect("directory:home")

        if User.objects.filter(username__iexact=name, is_active=False).exists():
            messages.warning(request, "Your registration is waiting for admin approval.")
        else:
            messages.error(request, "Invalid name or password.")

    return render(request, "login.html")


def reception_register(request):
    if request.user.is_authenticated:
        return redirect("directory:home")

    form = ReceptionRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["name"],
            password=form.cleaned_data["password"],
            is_active=False,
        )
        group, _ = Group.objects.get_or_create(name="Reception")
        user.groups.add(group)
        messages.success(
            request,
            "Registration submitted. You can log in after admin approval.",
        )
        return redirect("directory:login")

    return render(request, "register.html", {"form": form})


def reception_logout(request):
    logout(request)
    return redirect("directory:login")


@login_required
def home(request):
    context = {
        "district_count": District.objects.count(),
        "organizer_count": Organizer.objects.count(),
        "location_count": Location.objects.count(),
    }
    return render(request, "index.html", context)


def _similarity(left, right):
    return SequenceMatcher(None, left.lower(), right.lower()).ratio()


@require_GET
@login_required
def search_locations(request):
    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return JsonResponse({"results": []})

    terms = search_terms(query)
    filters = Q()
    for term in terms:
        filters |= (
            Q(name__icontains=term)
            | Q(aliases__icontains=term)
            | Q(district__name__icontains=term)
            | Q(organizer__name__icontains=term)
            | Q(organizer__phone_number__icontains=term)
            | Q(organizer__district__name__icontains=term)
        )

    locations = (
        Location.objects.select_related("district", "organizer", "organizer__district")
        .filter(filters)
        .order_by("name")[:25]
    )

    exactish_matches = list(locations)

    if len(exactish_matches) < 10:
        candidates = list(
            Location.objects.select_related("district", "organizer", "organizer__district")
            .only(
                "id",
                "name",
                "aliases",
                "district__name",
                "organizer__name",
                "organizer__phone_number",
                "organizer__district__name",
            )
            .order_by("name")
        )

        searchable_values = []
        for location in candidates:
            searchable_values.extend(
                [
                    location.name,
                    location.aliases,
                    location.organizer.name,
                    location.district.name if location.district else "",
                    location.organizer.district.name,
                ]
            )

        close_values = set()
        for term in terms:
            close_values.update(get_close_matches(term, searchable_values, n=35, cutoff=0.55))

        def best_score(location):
            values = [
                location.name,
                location.aliases,
                location.organizer.name,
                location.district.name if location.district else "",
                location.organizer.district.name,
            ]
            return max(_similarity(term, value) for term in terms for value in values if value)

        fuzzy_matches = [
            location
            for location in candidates
            if (
                location.name in close_values
                or location.aliases in close_values
                or location.organizer.name in close_values
                or (location.district and location.district.name in close_values)
                or location.organizer.district.name in close_values
                or best_score(location) >= 0.55
            )
        ]
        fuzzy_matches.sort(key=best_score, reverse=True)

        seen_ids = {location.id for location in exactish_matches}
        exactish_matches.extend(
            location for location in fuzzy_matches if location.id not in seen_ids
        )

    results = [
        {
            "location": location.name,
            "organizer": location.organizer.name,
            "phone": location.organizer.phone_number,
            "district": location.district.name if location.district else location.organizer.district.name,
        }
        for location in exactish_matches[:25]
    ]

    return JsonResponse({"results": results})
