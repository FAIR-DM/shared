"""URL configuration of the example portal."""

from django.urls import include, path

urlpatterns = [
    path("", include("fairdm.conf.urls")),
]
