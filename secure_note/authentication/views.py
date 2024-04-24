from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login, authenticate
from django.contrib.auth.models import User
from authentication.validation import validate_password


# Create your views here.
def index(requests):   
    if requests.user.is_authenticated:
        return HttpResponseRedirect(reverse("note:index"))
    return HttpResponseRedirect(reverse("authentication:login",))


def login_view(requests):
    message=""
    if requests.method == "POST":
        username = requests.POST["username"]
        password = requests.POST["password"]
        user = authenticate(requests, username=username, password=password)
        if user is not None:
            login(requests,user)
            return HttpResponseRedirect(reverse("note:index",))
        else:
            message = "invalid username and password"
    return render(requests,"authentication/login/index.html",{"message" : message})


def register(requests):
    message=""
    if requests.method == 'POST' and requests.POST.get("username") != "":
        if not ((validate_password(requests.POST.get("password1"))) and (requests.POST.get("password1") == requests.POST.get("password2"))):
            message = "The password is invalid\nMake sure it has captial and small letter with number and special character"
            return render(requests,"authentication/login/index.html",{"message":message,})
        try:
            user_temp = User.objects.get(username=requests.POST.get("username"))
        except:
            user = User.objects.create_user(requests.POST.get("username"), requests.POST.get("email"), requests.POST.get("password1"))
            user.first_name = requests.POST.get("firstname")
            user.last_name = requests.POST.get("lastname")
            user.save()
        else:
            message = "the username is taken"
    return render(requests,"authentication/login/index.html",{"message":message,})


@login_required(login_url="/login/")
def logout_views(requests):
    logout(requests)
    return HttpResponseRedirect(reverse("authentication:index",))


@login_required(login_url="/login/")
def password_reset(requests):
    if requests.method == "POST":
        if not (validate_password(requests.POST.get("password1"))):
            message = "The password is invalid\nMake sure it has captial and small letter with number and special character"
            return render(requests,"authentication/reset/index.html",{"message":message,})
        password1 = requests.POST.get("password1")
        password2 = requests.POST.get("password2")
        if password1 == password2 and password1 != "":
            user = requests.user
            user.set_password(password1)
            user.save()
            return HttpResponseRedirect(reverse("note:index",))
    return render(requests,"authentication/reset/index.html")


@login_required(login_url="/login/")
def update(requests):
    user = User.objects.get(username = requests.user.username)
    if requests.method == 'POST':
        try:
            user.first_name = requests.POST.get("firstname")
            
            user.last_name = requests.POST.get("lastname")
            
            user.email = requests.POST.get("email")
            user.save()
            return HttpResponseRedirect(reverse("note:index",))
        except:
            pass
    return render(requests,"authentication/reset/index.html",{"user":user})