from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect,Http404
from .forms import LoginForm,RegistrationForm,UpdateForm,PasswordResetForm,ForgetForm,CaptchaForm
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from user_defined.validation import validate_password,is_all_char,is_all_char_num
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import UserProfile
from user_defined import cryptoengine
import random


class Index(LoginRequiredMixin,View):
    login_url = "/login"
    def get(self, requests):
        return HttpResponsePermanentRedirect(reverse("note:index"))


class LoginView(View):
    def get(self,requests):
        form = CaptchaForm()
        return render(requests,"authentication/login/index.html",{"form":form})
    
    def post(self,requests):
        login_form = LoginForm(data=requests.POST)
        if login_form.is_valid():
            username = requests.POST["username"]
            password = requests.POST["password"]
            user = authenticate(requests, username=username, password=password)
            if user is not None:
                login(requests,user)
                return HttpResponsePermanentRedirect(reverse("note:index",))
        message = "Invalid username or password"
        return render(requests,"authentication/login/index.html",{"message" : message,"form":CaptchaForm()})


class RegistrationView(View):
    def get(self,requests):
        form = CaptchaForm()
        return render(requests,"authentication/login/index.html",{"form":form})

    def post(self,requests):
        registeration_form = RegistrationForm(data=requests.POST)
        if registeration_form.is_valid():
            message=""
            if not (validate_password(requests.POST.get("password1"))):
                message = "The password is invalid\nMake sure it has captial and small letter with number and special character"
            elif not requests.POST.get("password1") == requests.POST.get("password2"):
                message = "The password does not match"
            elif not is_all_char(requests.POST["firstname"] + requests.POST["lastname"]):
                message = "The name is invalid only use character"
            elif not is_all_char_num(requests.POST["username"]):
                message = "The username is invlaid only use alphabets and digit"
            else:
                try:
                    user_temp = User.objects.get(username=requests.POST.get("username"))
                except:
                    user = User.objects.create_user(requests.POST.get("username"), requests.POST.get("email"), requests.POST.get("password1"))
                    user.first_name = requests.POST.get("firstname")
                    user.last_name = requests.POST.get("lastname")
                    user.save()
                    file_path = cryptoengine.MessageDigest.sha256_hash(user.username + str(random.randbytes))
                    while len(UserProfile.objects.filter(file_path = file_path)) != 0:
                        file_path = cryptoengine.MessageDigest.sha256_hash(user.username + str(random.randbytes))
                    check = cryptoengine.RSACryptography.key_generation(file_path)
                    if check:
                        aes_secret_key = cryptoengine.AESCryptography.key_generation(requests.POST.get("password1"))
                        singed_aes_key = cryptoengine.RSACryptography.sign(aes_secret_key)
                        aes_rsa_encrytion = cryptoengine.RSACryptography.encryption(file_path,aes_secret_key)
                        user_profile = UserProfile(user_user=user,signed_password=singed_aes_key, hashed_password=aes_rsa_encrytion,file_path=file_path)
                        user_profile.save()
                    else:
                        return Http404()
                else:
                    message = "Username is taken"
        else:
            message = registeration_form.errors.as_text()
        return render(requests,"authentication/login/index.html",{"message":message,"form":CaptchaForm()})

class LogoutView(LoginRequiredMixin,View):
    login_url="/login/"
    def get(self,requests):
        logout(requests)
        return HttpResponsePermanentRedirect(reverse("authentication:index",))
    
class PasswordRestView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,requests):
        form = CaptchaForm()
        user = User.objects.get(id = requests.user.id)
        user_profile = UserProfile.objects.get(user_user = user)
        return render(requests,"authentication/reset/index.html",{"user":user,"user_profile":user_profile,"form":form})
    
    def post(self,requests):
        password_reset_form = PasswordResetForm(data=requests.POST)
        if password_reset_form.is_valid():
            message = ""
            if not (validate_password(requests.POST.get("password1"))):
                message = "The password is invalid\nMake sure it has captial and small letter with number and special character"
            elif requests.POST.get("password1") == requests.POST.get("password2"):
                user = requests.user
                user.set_password(requests.POST.get("password1"))
                user.save()
                return HttpResponsePermanentRedirect(reverse("note:index",))
            elif requests.POST.get("password1") != requests.POST.get("password2"):
                message = "The password field is not the same"
            elif requests.POST.get("password1") == "":
                message = "The password field is required"
        else:
            message = password_reset_form.errors.as_text()
        user = User.objects.get(id = requests.user.id)
        user_profile = UserProfile.objects.get(user_user = user)
        return render(requests,"authentication/reset/index.html",{"message":message,"user":user,"user_profile":user_profile,"form":CaptchaForm()})


class UpdateView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,requests):
        form = CaptchaForm()
        user = User.objects.get(id = requests.user.id)
        user_profile = UserProfile.objects.get(user_user = user)
        return render(requests,"authentication/reset/index.html",{"user":user,"user_profile":user_profile,"form":form})

    def post(self,requests):
        message = ""
        user = User.objects.get(id = requests.user.id)
        user_profile = UserProfile.objects.get(user_user = user)
        update_form = UpdateForm(requests.POST,requests.FILES)
        if update_form.is_valid():
            if not is_all_char(requests.POST["firstname"]) and not is_all_char(requests.POST["lastname"]):
                return Http404()
            else:
                user.first_name = requests.POST.get("firstname")
                user.last_name = requests.POST.get("lastname")
                user.email = requests.POST.get("email")
                user_profile.profile_picture = requests.FILES['profile_picture']
                user.save()
                user_profile.save()
                return HttpResponsePermanentRedirect(reverse("note:index",))
        else:
            message = "Invalid Input Make sure You use the right Thing"
        return render(requests,"authentication/reset/index.html",{"user":user,"user_profile":user_profile,"message1":update_form.errors.as_text(),"message":message,"form":CaptchaForm()})


class ForgetView(View):
    def get(self,requests):
        form = CaptchaForm()
        return render(requests,"authentication/forget/index.html",{"form",form})

    def post(self,requests):
        forget_form = ForgetForm(data=requests.POST)
        if forget_form.is_valid():
            return HttpResponsePermanentRedirect(reverse("authentication:index",))
        else:
            message = forget_form.errors.as_text()
            return render(requests,"authentication/forget/index.html",{"message":message,"form":CaptchaForm()})
        
    

class AboutView(View):
    def get(self,requests):
        return render(requests,"bio/index.html")