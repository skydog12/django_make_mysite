# main/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Admin, Student, ReligiousEvent, EventAttendance

class AdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Admin
        fields = UserCreationForm.Meta.fields + ('contact', 'religion', 'admin_type')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'password', 'grade', 'company', 'name', 'contact']
        widgets = {
            'password': forms.PasswordInput(),
        }

class ReligiousEventForm(forms.ModelForm):
    class Meta:
        model = ReligiousEvent
        fields = ['event_id', 'date', 'religion', 'status', 'reserved_count', 'attended_count', 'note']

class EventAttendanceForm(forms.ModelForm):
    class Meta:
        model = EventAttendance
        fields = ['reservation', 'attendance', 'note']