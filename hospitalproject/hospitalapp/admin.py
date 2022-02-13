from django.contrib import admin

# Register your models here.
from django import forms
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
# from .forms import CustomUserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.
from django.contrib.auth import get_user_model
from .models import Doctor,Department,DoctorTimeSlot,BookAppointment

User=get_user_model()


class DoctorAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','qualification','area_of_expertise','department','book_appointent','fees']

    def book_appointent(self,obj):
        return "\n".join([str(a.patinet_name) for a in obj.book_appointent.all()])


# class PatientAdmin(admin.ModelAdmin):
#     list_display=['name','phone','email']

class DepartmnetAdmin(admin.ModelAdmin):
    list_display=['department']

class DoctorTimeAdmin(admin.ModelAdmin):
    list_display=['doctor','date','start_time','end_time','booked','slots_available']

class BookAppointmentAdmin(admin.ModelAdmin):
    list_display=['mydoctor','start_time','end_time','patinet_name','patient_phone','patient_email','file_upload']


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ('email','is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','password','is_staff','is_active')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password','name','is_active')}),
        ('Permissions', {'fields': ('is_staff','is_superuser')}),
        ('Login', {'fields': ('last_login', )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password','is_active'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# admin.site.register(Patient,PatientAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Department,DepartmnetAdmin)
admin.site.register(DoctorTimeSlot,DoctorTimeAdmin)
admin.site.register(BookAppointment,BookAppointmentAdmin)
