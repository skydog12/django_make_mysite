# main/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import AdminCreationForm, StudentForm, ReligiousEventForm, EventAttendanceForm
from .models import Admin, Student, ReligiousEvent, EventAttendance
from django.db.models import Q

def home(request):
    upcoming_events = ReligiousEvent.objects.filter(status='예약').order_by('date')[:5]
    return render(request, 'home.html', {'upcoming_events': upcoming_events})

def admin_register(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            admin = form.save()
            login(request, admin)
            messages.success(request, '관리자 계정이 생성되었습니다.')
            return redirect('admin_events')
    else:
        form = AdminCreationForm()
    return render(request, 'admin_register.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and isinstance(user, Admin):
            login(request, user)
            messages.success(request, '로그인되었습니다.')
            return redirect('admin_events')
        else:
            messages.error(request, '잘못된 관리자 번호 또는 비밀번호입니다.')
    return render(request, 'admin_login.html')

def student_register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '학생 계정이 생성되었습니다.')
            return redirect('student_login')
    else:
        form = StudentForm()
    return render(request, 'student_register.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        password = request.POST['password']
        student = get_object_or_404(Student, student_id=student_id, password=password)
        login(request, student)
        messages.success(request, '로그인되었습니다.')
        return redirect('student_activities')
    return render(request, 'student_login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, '로그아웃되었습니다.')
    return redirect('home')

@login_required
def student_profile(request):
    if isinstance(request.user, Student):
        student = request.user
        if request.method == 'POST':
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, '프로필이 업데이트되었습니다.')
                return redirect('student_profile')
        else:
            form = StudentForm(instance=student)
        return render(request, 'student_profile.html', {'form': form})
    else:
        messages.error(request, '학생만 접근할 수 있습니다.')
        return redirect('home')

@login_required
def student_activities(request):
    if isinstance(request.user, Student):
        student = request.user
        attendances = EventAttendance.objects.filter(student=student)
        return render(request, 'student_activities.html', {'attendances': attendances})
    else:
        messages.error(request, '학생만 접근할 수 있습니다.')
        return redirect('home')

@login_required
def student_reservation(request):
    if isinstance(request.user, Student):
        student = request.user
        if request.method == 'POST':
            event_id = request.POST.get('event_id')
            event = get_object_or_404(ReligiousEvent, event_id=event_id)
            attendance, created = EventAttendance.objects.get_or_create(student=student, event=event)
            if created:
                messages.success(request, '예약이 완료되었습니다.')
            else:
                messages.info(request, '이미 예약된 행사입니다.')
            return redirect('student_activities')
        else:
            events = ReligiousEvent.objects.filter(status='예약')
            return render(request, 'student_reservation.html', {'events': events})
    else:
        messages.error(request, '학생만 접근할 수 있습니다.')
        return redirect('home')

@user_passes_test(lambda u: isinstance(u, Admin))
def admin_events(request):
    events = ReligiousEvent.objects.all()
    if request.method == 'POST':
        form = ReligiousEventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '종교행사가 등록되었습니다.')
            return redirect('admin_events')
    else:
        form = ReligiousEventForm()
    return render(request, 'admin_events.html', {'events': events, 'form': form})

@user_passes_test(lambda u: isinstance(u, Admin))
def admin_event_detail(request, event_id):
    event = get_object_or_404(ReligiousEvent, event_id=event_id)
    if request.method == 'POST':
        form = ReligiousEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, '종교행사 정보가 업데이트되었습니다.')
            return redirect('admin_events')
    else:
        form = ReligiousEventForm(instance=event)
    attendances = EventAttendance.objects.filter(event=event)
    return render(request, 'admin_event_detail.html', {'event': event, 'form': form, 'attendances': attendances})

@user_passes_test(lambda u: isinstance(u, Admin))
def admin_event_delete(request, event_id):
    event = get_object_or_404(ReligiousEvent, event_id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, '종교행사가 삭제되었습니다.')
        return redirect('admin_events')
    return render(request, 'admin_event_delete.html', {'event': event})

@user_passes_test(lambda u: isinstance(u, Admin))
def admin_attendance_update(request, attendance_id):
    attendance = get_object_or_404(EventAttendance, id=attendance_id)
    if request.method == 'POST':
        form = EventAttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, '참석 정보가 업데이트되었습니다.')
            return redirect('admin_event_detail', event_id=attendance.event.event_id)
    else:
        form = EventAttendanceForm(instance=attendance)
    return render(request, 'admin_attendance_update.html', {'form': form, 'attendance': attendance})

def search_events(request):
    query = request.GET.get('q')
    if query:
        events = ReligiousEvent.objects.filter(
            Q(event_id__icontains=query) |
            Q(religion__icontains=query) |
            Q(status__icontains=query)
        )
    else:
        events = ReligiousEvent.objects.all()
    return render(request, 'search_events.html', {'events': events, 'query': query})

# Create your views here.
