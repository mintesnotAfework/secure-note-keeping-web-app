from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import FileModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class IndexView(LoginRequiredMixin,View):
    login_url="/login/"
    def get(self,requests):
        list_of_file = FileModel.objects.filter(user=requests.user)
        return render(requests,"note/index.html",{"list_of_file":list_of_file})
    

class SaveFile(LoginRequiredMixin,View):
    login_url="/login/"
    def get(self,requests):
        return HttpResponseRedirect(reverse("note:index"))
    
    def post(self,requests):
        file_name = requests.POST.get('filename')
        file_content = requests.POST.get('filecontent')
        if (file_name is not None):
            try:
                temp = FileModel.objects.filter(user=requests.user).get(name=file_name)
                raise FileExistsError()
            except FileExistsError:
                m = temp
                m.content = file_content
                m.save()
            except:
                m = FileModel()
                m.name = file_name
                m.content = file_content
                m.user = requests.user
                m.save()
            return HttpResponseRedirect(reverse("note:file_display",args = (file_name,)))


class FileDisplayView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,requests,name):
        file = FileModel.objects.get(name=name)
        list_of_files = FileModel.objects.filter(user=requests.user)
        return render(requests,"note/index2.html",{"file":file,"list_of_file":list_of_files})


class DeleteFileView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,requests,name):
        if requests.method == "POST":
            file = FileModel.objects.get(name=name)
            file.delete()
        return HttpResponseRedirect(reverse("note:index"))
