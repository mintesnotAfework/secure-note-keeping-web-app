from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect,Http404,HttpResponseBadRequest
from django.urls import reverse
from .forms import SaveForm
from .models import FileModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from user_defined import cryptoengine, recovery
from authentication.models import UserProfile


class IndexView(LoginRequiredMixin,View):
    login_url="/login/"
    def get(self,requests):
        list_of_file = FileModel.objects.filter(user=requests.user)
        try:
            user_profile = UserProfile.objects.get(user_user = requests.user)
        except:
            return HttpResponsePermanentRedirect(reverse("authentication:logout"))
        return render(requests,"note/index.html",{"list_of_file":list_of_file,"user_password":user_profile})
    

class SaveFile(LoginRequiredMixin,View):
    login_url="/login/"
    def get(self,requests):
        return HttpResponsePermanentRedirect(reverse("note:index"))
    
    def post(self,requests):
        save_form = SaveForm(data=requests.POST)
        if save_form.is_valid():
            file_name = requests.POST.get('filename')
            file_content = requests.POST.get('filecontent')
            try:
                temp = FileModel.objects.filter(user=requests.user).get(name=file_name)
                raise FileExistsError()
            except FileExistsError:
                m = temp
                user_password = UserProfile.objects.get(user_user=requests.user)
                aes_password = cryptoengine.RSACryptography.decryption(user_password.file_path,user_password.hashed_password)
                check_validaty = cryptoengine.RSACryptography.verify_sign(aes_password,user_password.signed_password)
                if check_validaty:
                    m.content = cryptoengine.AESCryptography.encryption(aes_password,file_content.encode())
                else:
                    user_password = recovery.Recover.regenerateAESKey(requests.user,user_password)
                    aes_password = cryptoengine.RSACryptography.decryption(user_password.file_path,user_password.hashed_password)
                    check_validaty = cryptoengine.RSACryptography.verify_sign(aes_password,user_password.signed_password)
                    if check_validaty:
                        m.content = cryptoengine.AESCryptography.encryption(aes_password.file_content.encode())
                    else:
                        return HttpResponseBadRequest()
                m.sha256_hash = cryptoengine.MessageDigest.sha256_hash(file_content)
                m.md5_hash = cryptoengine.MessageDigest.md5_hash(file_content)
                m.save()
            except:
                m = FileModel()
                m.name = file_name
                user_password = UserProfile.objects.get(user_user=requests.user)
                aes_password = cryptoengine.RSACryptography.decryption(user_password.file_path,user_password.hashed_password)
                check_validaty = cryptoengine.RSACryptography.verify_sign(aes_password,user_password.signed_password)
                if check_validaty:
                    m.content = cryptoengine.AESCryptography.encryption(aes_password,file_content.encode())
                else:
                    user_password = recovery.Recover.regenerateAESKey(requests.user,user_password)
                    aes_password = cryptoengine.RSACryptography.decryption(user_password.file_path,user_password.hashed_password)
                    check_validaty = cryptoengine.RSACryptography.verify_sign(aes_password,user_password.signed_password)
                    if check_validaty:
                        m.content = cryptoengine.AESCryptography.encryption(aes_password.file_content.encode())
                    else:
                        return HttpResponseBadRequest()
                m.user = requests.user
                m.sha256_hash = cryptoengine.MessageDigest.sha256_hash(file_content)
                m.md5_hash = cryptoengine.MessageDigest.md5_hash(file_content)
                m.save()
            return HttpResponsePermanentRedirect(reverse("note:file_display",args = (file_name,)))
        else:
            return Http404()


class FileDisplayView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,requests,name):
        file = FileModel.objects.filter(user=requests.user).get(name=name)
        list_of_files = FileModel.objects.filter(user=requests.user)
        user_password = UserProfile.objects.get(user_user=requests.user)
        aes_password = cryptoengine.RSACryptography.decryption(user_password.file_path,user_password.hashed_password)
        check_validaty = cryptoengine.RSACryptography.verify_sign(aes_password,user_password.signed_password)
        if check_validaty:
            content = cryptoengine.AESCryptography.decryption(file.content,aes_password)
        else:
            user_password = recovery.Recover.regenerateAESKey(requests.user,user_password)
            aes_password = cryptoengine.RSACryptography.decryption(user_password.file_path,user_password.hashed_password)
            check_validaty = cryptoengine.RSACryptography.verify_sign(aes_password,user_password.signed_password)
            if check_validaty:
                content = cryptoengine.AESCryptography.encryption(aes_password.file_content.encode())
            else:
                return HttpResponseBadRequest()
        return render(requests,"note/index2.html",{"file":file,"list_of_file":list_of_files,"content":content.decode(),"user_password":user_password})


class DeleteFileView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,requests,name):   
        file = FileModel.objects.filter(user = requests.user).get(name=name)
        return render(requests,"note/delete_confirm.html",{"file":file})
    
    def post(self,requests,name):
        file = FileModel.objects.filter(user = requests.user).get(name=name)
        file.delete()
        return HttpResponsePermanentRedirect(reverse("note:index"))