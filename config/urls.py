from django.contrib import admin
from django.urls import include, path

import debug_toolbar

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("api/", include("project_manager.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
]
