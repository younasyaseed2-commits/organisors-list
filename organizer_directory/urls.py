from django.contrib import admin
from django.urls import include, path

from directory import admin_views

urlpatterns = [
    path("dashboard/login/", admin_views.admin_login, name="custom_admin_login"),
    path("dashboard/logout/", admin_views.admin_logout, name="custom_admin_logout"),
    path("dashboard/", admin_views.dashboard, name="custom_admin_dashboard"),
    path("dashboard/data-upload/", admin_views.data_upload, name="custom_admin_data_upload"),
    path("dashboard/manual-upload/", admin_views.manual_upload, name="custom_admin_manual_upload"),
    path("dashboard/reception-users/", admin_views.reception_users, name="custom_admin_users"),
    path("admin/data-upload/", admin_views.data_upload, name="admin_data_upload"),
    path("admin/", admin.site.urls),
    path("", include("directory.urls")),
]
