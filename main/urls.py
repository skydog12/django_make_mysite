from django.urls import path
from . import views

urlpatterns = [
    path('admin/register/', views.admin_register, name='admin_register'),
    path('student/register/', views.student_register, name='student_register'),
    path('admin/events/', views.admin_events, name='admin_events'),
    path('admin/events/<int:event_id>/', views.admin_event_detail, name='admin_event_detail'),
    path('admin/events/attendance/<int:attendance_id>/', views.admin_attendance_update, name='admin_attendance_update'),
    path('student/activities/', views.student_activities, name='student_activities'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/reservation/', views.student_reservation, name='student_reservation'),
    path('search/events/', views.search_events, name='search_events'),
    path('', views.home, name='home'),
    # 추가적인 URL 패턴들...
]
