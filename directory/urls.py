from django.urls import path

from . import views

app_name = "directory"

urlpatterns = [
    path("login/", views.reception_login, name="login"),
    path("register/", views.reception_register, name="register"),
    path("logout/", views.reception_logout, name="logout"),
    path("", views.home, name="home"),
    path("ajax/search-locations/", views.search_locations, name="search_locations"),
]
