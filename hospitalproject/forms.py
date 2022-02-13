from hospitalapp.models import CustomUser
from django import forms
class User(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('email','password')