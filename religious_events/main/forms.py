from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyAdmin, Student, ReligiousEvent, EventAttendance

# MyAdmin 모델의 사용자 생성을 위한 폼
class MyAdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyAdmin
        # 사용자 생성 시 추가할 필드들
        fields = UserCreationForm.Meta.fields + ('contact', 'religion', 'admin_type')

# Student 모델을 위한 폼
class StudentForm(forms.ModelForm):
    # 비밀번호 필드를 추가
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        # 폼에 포함될 필드들
        fields = ['student_id', 'password', 'grade', 'company', 'name', 'contact', 'note']

# ReligiousEvent 모델을 위한 폼
class ReligiousEventForm(forms.ModelForm):
    class Meta:
        model = ReligiousEvent
        # 폼에 포함될 필드들
        fields = ['event_id', 'date', 'religion', 'status', 'reserved_count', 'attended_count', 'note']

# EventAttendance 모델을 위한 폼
class EventAttendanceForm(forms.ModelForm):
    class Meta:
        model = EventAttendance
        # 폼에 포함될 필드들
        fields = ['reservation', 'attendance', 'note']

# 학생 로그인 폼
class StudentLoginForm(forms.Form):
    student_id = forms.CharField(max_length=7)  # 학번 필드
    password = forms.CharField(widget=forms.PasswordInput)  # 비밀번호 필드


class StudentProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Student
        fields = ['grade', 'company', 'name', 'contact', 'note']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

        return cleaned_data
