from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import FileModel
from django.contrib import Views

# Create your views here.
@login_required(login_url="/login/")
def index(requests):
    list_of_file = FileModel.objects.filter(user=requests.user)
    return render(requests,"note/index.html",{"list_of_file":list_of_file})


@login_required(login_url="/login/")
def save_file(requests):
    if requests.method == 'POST':
        file_name = requests.POST.get('filename')
        file_content = requests.POST.get('filecontent')
        if (file_name is not None):
            try:
                temp = FileModel.objects.get(name=file_name)
                if temp.user == requests.user:
                    print("mintens jsdlkfjsak")
                    raise IndexError()
            except IndexError:
                m = FileModel.objects.get(name = file_name)
                m.content = file_content
                m.save()
                print(m.content)
            except:
                m = FileModel()
                m.name = file_name
                m.content = file_content
                m.user = requests.user
                m.save()
            return HttpResponseRedirect(reverse("note:file_display",args = (file_name,)))
    return HttpResponseRedirect(reverse("note:index"))


@login_required(login_url="/login/")
def file_display(requests, name):
    file = FileModel.objects.get(name=name)
    list_of_files = FileModel.objects.filter(user=requests.user)
    return render(requests,"note/index2.html",{"file":file,"list_of_file":list_of_files})


@login_required(login_url="/login/")
def delete_file(requests,name):
    if requests.method == "POST":
        file = FileModel.objects.get(name=name)
        file.delete()
    return HttpResponseRedirect(reverse("note:index"))