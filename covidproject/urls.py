from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('slots.urls')),
    path('admin/', admin.site.urls),
]