from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyAdmin, Student, ReligiousEvent, EventAttendance

# MyAdmin 모델을 위한 어드민 클래스
class MyAdminAdmin(UserAdmin):
    model = MyAdmin
    # 어드민 페이지에서 표시할 필드들
    list_display = ['username', 'email', 'contact', 'religion', 'admin_type', 'is_staff']
    # 어드민 페이지의 필드 구성 설정
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('contact', 'religion', 'admin_type')}),
    )
    # 새로운 MyAdmin 객체를 추가할 때 사용할 필드 구성 설정
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('contact', 'religion', 'admin_type')}),
    )

# Student 모델을 위한 어드민 클래스
class StudentAdmin(admin.ModelAdmin):
    # 어드민 페이지에서 표시할 필드들
    list_display = ['student_id', 'name', 'grade', 'company', 'contact']
    # 검색을 위한 필드들
    search_fields = ['student_id', 'name']

# ReligiousEvent 모델을 위한 어드민 클래스
class ReligiousEventAdmin(admin.ModelAdmin):
    # 어드민 페이지에서 표시할 필드들
    list_display = ['event_id', 'date', 'religion', 'status', 'reserved_count', 'attended_count']
    # 필터를 위한 필드들
    list_filter = ['religion', 'status']
    # 검색을 위한 필드들
    search_fields = ['event_id', 'date']

# EventAttendance 모델을 위한 어드민 클래스
class EventAttendanceAdmin(admin.ModelAdmin):
    # 어드민 페이지에서 표시할 필드들
    list_display = ['student', 'event', 'reservation', 'attendance']
    # 필터를 위한 필드들
    list_filter = ['reservation', 'attendance']
    # 검색을 위한 필드들
    search_fields = ['student__student_id', 'student__name', 'event__event_id']

# 모델들을 어드민 사이트에 등록
admin.site.register(MyAdmin, MyAdminAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(ReligiousEvent, ReligiousEventAdmin)
admin.site.register(EventAttendance, EventAttendanceAdmin)
# 모델들을 여기서 등록합니다.
