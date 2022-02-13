from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import pytz
import datetime
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractBaseUser,PermissionsMixin):
    
    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(verbose_name="email",max_length=60,unique=True)
    password=models.CharField(max_length=6,unique=True)
    is_active= models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects=CustomUserManager()





DEPARTMENT_CHOICES=(('Dental','Dental'),
                    ('Cardiology','Cardiology'),
                    ('Urology','Urology'),
                    ('Plastic Surgery','Plastic Surgery'),
                    ('Nerology','Nerology'))

class Department(models.Model):
    department=models.CharField(max_length=264,choices=DEPARTMENT_CHOICES,default='')

    def __str__(self):
        return self.department



# class Patient(models.Model):
#     name=models.CharField(max_length=50,null=True,blank=True)
#     phone=models.IntegerField(max_length=50,null=True,blank=True)
#     email = models.EmailField(verbose_name="email",max_length=60,unique=True)

    # def __str__(self):
    #         return self.name




class Doctor(models.Model):
    first_name=models.CharField(max_length=50,null=True,blank=True)
    last_name=models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(verbose_name="email",max_length=60)
    qualification=models.CharField(max_length=264,null=True,blank=True)
    area_of_expertise=models.CharField(max_length=264,null=True,blank=True)
    book_appointent=models.ManyToManyField('BookAppointment',symmetrical=False,default='',blank=True,null=True)  
    fees=models.IntegerField(null=True,blank=True)
    department=models.ForeignKey(Department,default='',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.first_name)

  
    # def __str__(self):
    #     return str(self.patient.all())


# class Appointment(models.Models):
#     doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
#     patinet_name=models.CharField(max_length=50,null=True,blank=True)
#     patient_phone=models.IntegerField(max_length=50,null=True,blank=True)
#     patient_email = models.EmailField(verbose_name="email",max_length=60,unique=True)
#     time_slot=models.DateTimeField(blank=True)

class DoctorTimeSlot(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date=models.DateField(null=True,blank=True)
    start_time=models.TimeField(null=True,blank=True)
    end_time=models.TimeField(null=True,blank=True)
    booked=models.BooleanField(default=False)
    slots_available=models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return str(self.start_time)
    

# @receiver(post_save,sender=DoctorTimeSlot)
# def save_doctortimeslot(sender,instance,created,**kwargs):
#     doctor=DoctorTimeSlot.objects.get(id=instance.id)
#     start_time=str(doctor.start_time)
#     end_time=str(doctor.end_time)
#     def time_slots(start_time, end_time):
#         print(start_time,type(start_time))
#         print(end_time,type(end_time))
#         t = start_time
#         while t <= end_time:
#             yield t.strftime('%H:%M:%S')
#             t = (datetime.datetime.combine(datetime.date.today(), t) +
#                 datetime.timedelta(minutes=15)).time()
#     t1,m1,s1=int(start_time[:2]),int(start_time[3:5]),int(start_time[6:9])
#     t2,m2,s2=int(end_time[:2]),int(end_time[3:5]),int(end_time[6:9])
#     start_time=datetime.time(t1,m1,s1)
#     end_time=datetime.time(t2,m2,s2)
#     print(list(time_slots(start_time,end_time)))

# post_save.connect(save_doctortimeslot,sender=DoctorTimeSlot)



class BookAppointment(models.Model):
    mydoctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    start_time=models.TimeField(default=timezone.now())
    end_time=models.TimeField(default=timezone.now())
    patinet_name=models.CharField(max_length=50,null=True,blank=True)
    patient_phone=models.CharField(max_length=10,null=True,blank=True)
    patient_email = models.EmailField(verbose_name="email",max_length=60,unique=True)
    file_upload=models.FileField(upload_to='documents')

    
    











   







