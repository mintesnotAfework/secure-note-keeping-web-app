from django import forms

class SaveForm(forms.Form):
    filecontent = forms.CharField(max_length=10000,min_length=1,required=True)
    filename = forms.CharField(max_length=64,min_length=2,required=True)