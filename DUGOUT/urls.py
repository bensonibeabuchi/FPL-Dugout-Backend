from django.contrib import admin
from django.urls import path, include,re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("fpl.urls")),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
]
