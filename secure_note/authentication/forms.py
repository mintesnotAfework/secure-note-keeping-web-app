from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64,min_length=5,required=True)
    password = forms.CharField(max_length=50,min_length=8,required=True)

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=64,min_length=5,required=True)
    password1 = forms.CharField(max_length=50,min_length=8,required=True)
    password2 = forms.CharField(max_length=50,min_length=8,required=True)
    email = forms.EmailField(max_length=320,min_length=5)
    firstname = forms.CharField(max_length=64,min_length=5,required=True)
    lastname = forms.CharField(max_length=64,min_length=5,required=True)

class UpdateForm(forms.Form):
    profile_picture = forms.ImageField(required=True)
    firstname = forms.CharField(max_length=64,min_length=5,required=True)
    lastname = forms.CharField(max_length=64,min_length=5,required=True)
    email = forms.EmailField(max_length=320,min_length=5,required=True)



class PasswordResetForm(forms.Form):
    password1 = forms.CharField(max_length=50,min_length=8,required=True)
    password2 = forms.CharField(max_length=50,min_length=8,required=True)

class ForgetForm(forms.Form):
    email = forms.EmailField(max_length=320,min_length=5)
