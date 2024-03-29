from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('appointments/', include(('appointment.urls', 'appointments'), namespace='appointments')),
    path('accounts/', include('allauth.urls')),
]