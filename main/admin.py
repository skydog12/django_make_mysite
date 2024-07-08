# main/admin.py

from django.contrib import admin
from .models import Admin, Student, ReligiousEvent, EventAttendance

admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(ReligiousEvent)
admin.site.register(EventAttendance)
# Register your models here.
