"""todolist URL Configuration"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('api/core/', include('core.urls')),
    path('goals/', include('goals.urls')),
    path('api/goals/', include('goals.urls')),
    path('bot/', include('bot.urls')),
    path('api/bot/', include('bot.urls')),
    path('oauth/', include("social_django.urls", namespace="social")),
]
