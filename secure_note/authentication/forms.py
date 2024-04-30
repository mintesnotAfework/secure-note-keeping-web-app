from django import forms
from captcha.fields import CaptchaField


class CaptchaForm(forms.Form):
    capcha = CaptchaField()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64,min_length=5,required=True)
    password = forms.CharField(max_length=50,min_length=8,required=True)

class RegistrationForm(CaptchaForm):
    username = forms.CharField(max_length=64,min_length=5,required=True)
    password1 = forms.CharField(max_length=50,min_length=8,required=True)
    password2 = forms.CharField(max_length=50,min_length=8,required=True)
    email = forms.EmailField(max_length=320,min_length=5)
    firstname = forms.CharField(max_length=64,min_length=5,required=True)
    lastname = forms.CharField(max_length=64,min_length=5,required=True)

class UpdateForm(CaptchaForm):
    profile_picture = forms.ImageField(required=True)
    firstname = forms.CharField(max_length=64,min_length=5,required=True)
    lastname = forms.CharField(max_length=64,min_length=5,required=True)
    email = forms.EmailField(max_length=320,min_length=5,required=True)



class PasswordResetForm(CaptchaForm):
    password1 = forms.CharField(max_length=50,min_length=8,required=True)
    password2 = forms.CharField(max_length=50,min_length=8,required=True)

class ForgetForm(CaptchaForm):
    email = forms.EmailField(max_length=320,min_length=5)


