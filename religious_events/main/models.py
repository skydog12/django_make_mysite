from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class MyAdmin(AbstractUser):
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

class Student(models.Model):
    student_id = models.CharField(max_length=7, primary_key=True)
    password = models.CharField(max_length=128)  # 해시된 비밀번호를 저장하기 위해 길이를 늘립니다
    grade = models.CharField(max_length=2)
    company = models.CharField(max_length=1)
    name = models.CharField(max_length=10)
    contact = models.CharField(max_length=12, blank=True)
    note = models.CharField(max_length=200, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.student_id
    class Meta:
        db_table = 'student'  # 기존 테이블 이름을 유지하려면 이 줄을 추가하세요
class ReligiousEvent(models.Model):
    RELIGION_CHOICES = [
        ('원불교', '원불교'),
        ('천주교', '천주교'),
        ('기독교', '기독교'),
        ('불교', '불교'),
    ]
    STATUS_CHOICES = [
        ('예약', '예약'),
        ('종료', '종료'),
        ('취소', '취소'),
    ]
    event_id = models.CharField(max_length=20, primary_key=True)
    date = models.CharField(max_length=10)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='예약')
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
