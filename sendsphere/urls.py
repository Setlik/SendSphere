from django.contrib import admin
from django.urls import include, path
from newsletter import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("newsletter/", include("newsletter.urls")),
    path("users/", include("users.urls")),
    path("", views.HomeView.as_view(), name="home"),
    path("tinymce/", include("tinymce.urls")),
]
