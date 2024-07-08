# main/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser


class Admin(AbstractUser):
    RELIGION_CHOICES = [
        ('원불교', '원불교'),
        ('천주교', '천주교'),
        ('기독교', '기독교'),
        ('불교', '불교'),
        ('전체', '전체'),
    ]
    ADMIN_TYPE_CHOICES = [
        ('군종', '군종'),
        ('훈육요원', '훈육요원'),
        ('대표생도', '대표생도'),
        ('지휘근무생도', '지휘근무생도'),
    ]

    contact = models.CharField(max_length=12, blank=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES)
    admin_type = models.CharField(max_length=20, choices=ADMIN_TYPE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='admin_user_set',  # 고유한 related_name 추가
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='admin_permission_set',  # 고유한 related_name 추가
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        verbose_name = 'admin'
        verbose_name_plural = 'admins'
class Student(models.Model):
    student_id = models.CharField(max_length=7, primary_key=True)
    password = models.CharField(max_length=20)
    grade = models.CharField(max_length=2)
    company = models.CharField(max_length=1)
    name = models.CharField(max_length=10)
    contact = models.CharField(max_length=12, blank=True)
    note = models.CharField(max_length=200, blank=True)


class ReligiousEvent(models.Model):
    EVENT_STATUS_CHOICES = [
        ('예약', '예약'),
        ('종료', '종료'),
        ('취소', '취소'),
    ]
    RELIGION_CHOICES = [
        ('원불교', '원불교'),
        ('천주교', '천주교'),
        ('기독교', '기독교'),
        ('불교', '불교'),
    ]

    event_id = models.CharField(max_length=20, primary_key=True)
    date = models.DateField()
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES)
    status = models.CharField(max_length=10, choices=EVENT_STATUS_CHOICES, default='예약')
    reserved_count = models.IntegerField(null=True, blank=True)
    attended_count = models.IntegerField(null=True, blank=True)
    note = models.CharField(max_length=200, blank=True)


class EventAttendance(models.Model):
    RESERVATION_CHOICES = [
        ('예약', '예약'),
        ('취소', '취소'),
    ]
    ATTENDANCE_CHOICES = [
        ('불참', '불참'),
        ('참석', '참석'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(ReligiousEvent, on_delete=models.CASCADE)
    reservation = models.CharField(max_length=10, choices=RESERVATION_CHOICES, default='예약')
    attendance = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, default='불참')
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('student', 'event')
# Create your models here.
