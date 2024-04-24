from django.urls import path
from . import views

app_name = "note"
urlpatterns =[
    path("",views.IndexView.as_view(),name="index"),
    path("save/",views.SaveFile.as_view(),name="save"),
    path("<str:name>/",views.FileDisplayView.as_view(),name="file_display"),
    path("delete/<str:name>/",views.DeleteFileView.as_view(),name="delete"),
]