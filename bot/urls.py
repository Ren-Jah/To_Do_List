from django.urls import path
from bot import views

urlpatterns = [
    path("virify", views.BotVerifyView.as_view()),
]