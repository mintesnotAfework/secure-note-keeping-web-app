from django.urls import path
from . import views


app_name = "authentication"
urlpatterns = [
    path("",views.index,name="index"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_views,name="logout"),
    path("register/",views.register,name="register"),
    path("password_reset/",views.password_reset,name="password_reset"),
    path("update/",views.update,name="update"),
]

