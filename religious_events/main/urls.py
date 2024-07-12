# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-register/', views.admin_register, name='admin_register'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('student-register/', views.student_register, name='student_register'),
    path('student-login/', views.student_login, name='student_login'),
    path('student-logout/', views.student_logout, name='student_logout'),
    path('logout/', views.logout_view, name='logout'),
    path('student-profile/', views.student_profile, name='student_profile'),
    path('student-activities/', views.student_activities, name='student_activities'),
    path('student-reservation/', views.student_reservation, name='student_reservation'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-events/', views.admin_events, name='admin_events'),
    path('admin-student-activities/', views.admin_student_activities, name='admin_student_activities'),
    path('admin-student-profiles/', views.admin_student_profiles, name='admin_student_profiles'),
    path('admin-event/<str:event_id>/', views.admin_event_detail, name='admin_event_detail'),
    path('admin-event-delete/<str:event_id>/', views.admin_event_delete, name='admin_event_delete'),
    path('admin-attendance-update/<int:attendance_id>/', views.admin_attendance_update, name='admin_attendance_update'),
    path('search-events/', views.search_events, name='search_events'),
]