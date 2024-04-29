"""
URL configuration for secure_note project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls,name="admin"),
    path("password-reset/", 
         views.PasswordResetView.as_view(template_name="authentication/forget/password_reset.html"),
         name="password_reset"),
    path("password-reset/done/", 
         views.PasswordResetDoneView.as_view(template_name="authentication/forget/password_reset_done.html"),
         name="password_reset_done"),
    # path(),
    # path(),
    path('',include('authentication.urls'),name="authentication"),
    path("note/",include("note.urls"),name="note"),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #static file addition from the setting file indjango 
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) #media file addition from the setting file indjango 