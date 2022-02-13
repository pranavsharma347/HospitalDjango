from django import forms
from .models import CustomUser,Doctor,BookAppointment


from django.contrib.auth import get_user_model


class User(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('email','password')

class DoctorUpdate(forms.ModelForm):
    class Meta:
        model=Doctor
        exclude =(' book_appointent',)

class AddDoctor(forms.ModelForm):
    class Meta:
        model=Doctor
        exclude =('book_appointent',)

class UpdatePatient(forms.ModelForm):
    class Meta:
        model=BookAppointment
        fields="__all__"

class AddApointment(forms.ModelForm):
    class Meta:
        model=BookAppointment
        fields="__all__"
        