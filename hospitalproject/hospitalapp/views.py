from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .backends import UserAuthenticate
from .forms import User,DoctorUpdate,AddDoctor,UpdatePatient,AddApointment
from .models import Doctor,BookAppointment,DoctorTimeSlot,CustomUser
from django.http import HttpResponse,JsonResponse,FileResponse,HttpResponseRedirect
from django.core import serializers
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
import string
import random
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile


#for generating password
def generate_password():
      data=''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(6))
      return data

# Create your views here

def homepage(request):
    return render(request,'base.html')

@login_required(login_url='login')
def head(request):
     return render(request,'adminpage.html')

def my_login(request):
    form=User()
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        check_user=UserAuthenticate()
        myuser=check_user.authenticate(email,password)
        if myuser is not None and myuser.is_superuser:
            login(request,myuser)
            print(request.user)
            return redirect('head')
        elif myuser is not None:
            login(request,myuser)
            print(request.user)
            return redirect('personaldoctor')
        elif myuser is None:
            messages.warning(request,'email/password is invalid')
    return render(request,'login.html',{'form':form})

@login_required(login_url='login')
def doctor(request):
    print('user',request.user)
    print('hai')
    doctor=Doctor.objects.all()
    return render(request,'doctor.html',{'doctor':doctor})

@login_required(login_url='login')
def patient(request):
    patients=BookAppointment.objects.all()
    return render(request,'patient.html',{'patients':patients})

@login_required(login_url='login')
def department(request):
    if request.method=="GET":
      department=request.GET['select']
      doctor=Doctor.objects.filter(department=department)
      return render(request,'doctor.html',{'doctor':doctor})

@login_required(login_url='login')
def doctorupdate(request,id):
    doctor=Doctor.objects.get(id=id)
    form=DoctorUpdate(instance=doctor)
    if request.method=='POST':
       forms=DoctorUpdate(request.POST,instance=doctor)
       if forms.is_valid():
           forms.save()
    return render(request,'doctorupdate.html',{'form':form})

@login_required(login_url='login')
def adddoctor(request):
    form=AddDoctor()
    if request.method=='POST':
        form=AddDoctor(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            print(email)
            try:
                user=CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                mypassword=generate_password()
                print(mypassword)
                password=make_password(mypassword,hasher='default',salt=None)
                custom=CustomUser(email=email,password=password)
                custom.save()
                form.save()
                print('email',email)
                print('password',mypassword)
                messages.success(request,'doctor add successfully')
                return render(request,'adddoctor.html',{'form':form})
            else:
                messages.success(request,'email already exist choose a unique email')
                return render(request,'adddoctor.html',{'form':form})
    return render(request,'adddoctor.html',{'form':form})
    

@login_required(login_url='login')
def deletedoctor(request,id):
    doctor=Doctor.objects.all()
    my_doctor=Doctor.objects.get(id=id)
    my_doctor.delete()
    return render(request,'doctor.html',{'doctor':doctor})

@login_required(login_url='login')
def updatepatient(request,id):
    patient=BookAppointment.objects.get(id=id)
    form=UpdatePatient(instance=patient)
    if request.method=='POST':
        form=UpdatePatient(request.POST,instance=patient)
        if form.is_valid():
            form.save()
    return render(request,'updatepatient.html',{'form':form})

@login_required(login_url='login')
def deletepatient(request,id):
    patients=BookAppointment.objects.all()
    patient=BookAppointment.objects.get(id=id)
    patient.delete()
    return render(request,'patient.html',{'patients':patients})


def homedoctors(request):
    if request.method=="GET":
        department=request.GET.get('select',None)
        doctor=Doctor.objects.filter(department=department)
        return render(request,'homedoctor.html',{'doctor':doctor})

@login_required(login_url='login')
def timeslots(request,id):
    doctor=Doctor.objects.get(id=id)
    timeslot=DoctorTimeSlot.objects.filter(doctor=doctor)
    return render(request,'timeslots.html',{'timeslot':timeslot})


def book_appointment(request):
    timeslot=Doctor.objects.all()
    doctor=DoctorTimeSlot.objects.filter(doctor__in=timeslot)
    if request.method=='POST':
        doctor=request.POST.get('mydoctor',None)
        time=request.POST.get('mytimeslot',None)
        patientname=request.POST.get('patientname',None)
        patientphone=request.POST.get('patientphone',None)
        patientemail=request.POST.get('patientemail',None)
        start_time=time[0:8]
        end_time=time[9:]
        doctorid=Doctor.objects.get(id=doctor)
        data=DoctorTimeSlot.objects.filter(doctor=doctorid).filter(start_time=start_time).filter(end_time=end_time).filter(slots_available=0).first()
        if data:
            data.booked=True
            data.save()
            messages.success(request,'all available slot is booked on that date')
            return render(request,'bookappointment.html',{'doctor':doctor,'timeslot':timeslot})
        else:        
            mydoctor=BookAppointment(mydoctor=doctorid,start_time=start_time,end_time=end_time,
            patinet_name=patientname,patient_phone=patientphone,patient_email=patientemail)
            mydoctor.save()
            messages.success(request,'appointment booked successfully')
            timeslot=DoctorTimeSlot.objects.filter(doctor=doctorid).filter(start_time=start_time).filter(end_time=end_time)
            for x in timeslot:
                if x.slots_available > 0:
                    x.slots_available=x.slots_available-1
                    x.save()
    return render(request,'bookappointment.html',{'doctor':doctor,'timeslot':timeslot})


def select_slot(request):
    if request.method=='GET' and request.is_ajax():
        select_doctor=request.GET.get('id',None)
        doctor=Doctor.objects.get(id=select_doctor)
        mydoctor=DoctorTimeSlot.objects.filter(doctor=doctor)
        list=[]
        for data in mydoctor:
            dict={}
            dict['id']=data.id
            dict['start_time']=data.start_time
            dict['end_time']=data.end_time
            list.append(dict)
        # data=serializers.serialize('json',doctor)
        return JsonResponse(list,safe=False)

def my_logout(request):
    logout(request)
    return redirect('/')



# def venue_pdf(data):
#     #Create Bytestream  buffer
#     buf=io.BytesIO()
#     #create a canvas
#     c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
#     #create a text object
#     textob=c.beginText()
#     textob.setTextOrigin(inch,inch)
#     textob.setFont("Helvetica",14)
#     #add some lines of code
#     textob.textLine(data)


#     c.drawText(textob)
#     c.showPage()
#     c.save()
#     buf.seek(0)
#     print(buf)
#     print('working')
#     return FileResponse(buf,as_attachment=True,filename='venue.pdf')


def personaldoctor(request):
    print('personal doctor',request.user)
    doctor=Doctor.objects.get(email='uma@gmail.com')
    return render(request,'personaldoctor.html',{'doctor':doctor})

def patientdoctor(request):
    print('patient doctor',request.user)
    doctor=Doctor.objects.get(email='uma@gmail.com')
    patient=BookAppointment.objects.filter(mydoctor=doctor)
    return render (request,'doctorpatient.html',{'patient':patient})

def write_report(request,id):
    print('write_report',request.user)
    patient=BookAppointment.objects.get(id=2)
    if request.method=='POST':
        data=request.POST.get('textarea',None)
        print(data)
        text=data.splitlines()
        print(text)
        
        buf=io.BytesIO()
        #create a canvas
        c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
        #create a text object
        textob=c.beginText()
        textob.setTextOrigin(inch,inch)
        textob.setFont("Helvetica",14)
        #add some lines of code
        for text in text:
            textob.textLine(text)
    
        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)
        pdf=buf.getvalue()
        file_data=ContentFile(pdf)
        data=BookAppointment.objects.get(id=2)
        data.file_upload.save('2.pdf',file_data,save=False)
        data.save()
    return render(request,'writereport.html')


    

    







    
