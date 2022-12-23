from django.urls import include, path
from core import views

urlpatterns = [
    path("signup", views.RegistrationView.as_view()),
    path("login", views.LoginView.as_view()),
    path("profile", views.ProfileView.as_view()),
    path("update_password", views.UpdatePasswordView.as_view()),
]
