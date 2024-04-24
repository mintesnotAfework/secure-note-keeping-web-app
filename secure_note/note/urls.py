from django.urls import path
from . import views

app_name = "note"
urlpatterns =[
    path("",views.index,name="index"),
    path("save/",views.save_file,name="save"),
    path("<str:name>/",views.file_display,name="file_display"),
    path("delete/<str:name>/",views.delete_file,name="delete"),
]