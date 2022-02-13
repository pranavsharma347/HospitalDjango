from django.urls import path
from .views import *

urlpatterns = [
    path('',homepage,name='homepage'),
    path('login/',my_login,name='login'),
    path('head/',head,name='head'),
    path('doctor/',doctor,name='doctor'),
    path('patient/',patient,name='patient'),
    path('department/',department,name="department"),
    path('doctorupdate/<int:id>/',doctorupdate,name="doctorupdate"),
    path('adddoctor/',adddoctor,name='adddoctor'),
    path('deletedoctor/<int:id>/',deletedoctor,name='deletedoctor'),
    path('updatepatient/<int:id>/',updatepatient,name='updatepatient'),
    path('deletepatient/<int:id>/',deletepatient,name='deletepatient'),
    path('homedoctors/',homedoctors,name='homedoctors'),
    path('timeslots/<int:id>/',timeslots,name='timeslot'),
    path('mybookappointment/',book_appointment,name='book_appointment'),
    # path('selecttimeslot/<int:id>/',select_slot,name='selectslot')
    path('selecttimeslot/',select_slot,name='selecttimesslot'),
    path('logout/',my_logout,name='logout'),
    # path('pdf/',venue_pdf,name='venue_pdf'),
    path('personaldoctor/',personaldoctor,name='personaldoctor'),
    path('doctorpatient/',patientdoctor,name='patientdoctor'),
    path('writereport/<int:id>/',write_report,name='writereport')
]   