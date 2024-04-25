from django.urls import path
from . import views


app_name = "authentication"
urlpatterns = [
    path("",views.Index.as_view(),name="index"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
    path("register/",views.RegistrationView.as_view(),name="register"),
    path("password_reset/",views.PasswordRestView.as_view(),name="password_reset"),
    path("update/",views.UpdateView.as_view(),name="update"),
    path("forget/",views.ForgetView.as_view(),name="forget"),
    path("about/",views.AboutView.as_view(),name="about"),
]

