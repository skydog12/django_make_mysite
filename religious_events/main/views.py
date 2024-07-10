from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import MyAdminCreationForm, StudentForm, ReligiousEventForm, EventAttendanceForm, StudentLoginForm, StudentProfileForm
from .models import MyAdmin, Student, ReligiousEvent, EventAttendance
from django.db.models import Q
from functools import wraps
# views.py

# ... (기존 import 문 유지)

def home(request):
    upcoming_events = ReligiousEvent.objects.filter(status='예약').order_by('date')[:5]
    return render(request, 'home.html', {'upcoming_events': upcoming_events})

def admin_register(request):
    if request.method == 'POST':
        form = MyAdminCreationForm(request.POST)
        if form.is_valid():
            admin = form.save()
            login(request, admin)
            messages.success(request, '관리자 계정이 생성되었습니다.')
            return redirect('admin_dashboard')
    else:
        form = MyAdminCreationForm()
    return render(request, 'admin_register.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and isinstance(user, MyAdmin):
            login(request, user)
            request.session['admin_id'] = user.id  # 세션에 관리자 ID 저장
            messages.success(request, '로그인되었습니다.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, '잘못된 관리자 번호 또는 비밀번호입니다.')
    return render(request, 'admin_login.html')
def student_register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.set_password(form.cleaned_data['password'])
            student.save()
            messages.success(request, '학생 계정이 생성되었습니다.')
            return redirect('student_login')
    else:
        form = StudentForm()
    return render(request, 'student_register.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            password = form.cleaned_data['password']
            student = Student.objects.filter(student_id=student_id).first()
            if student and student.check_password(password):
                # 세션에 학생 정보 저장
                request.session['student_id'] = student.student_id
                request.session['student_name'] = student.name
                messages.success(request, '로그인되었습니다.')
                return redirect('student_activities')
            else:
                messages.error(request, '잘못된 교번 또는 비밀번호입니다.')
    else:
        form = StudentLoginForm()
    return render(request, 'student_login.html', {'form': form})
def student_logout(request):
    # 세션에서 학생 정보 삭제
    request.session.pop('student_id', None)
    request.session.pop('student_name', None)
    messages.success(request, '로그아웃되었습니다.')
    return redirect('home')  # 또는 다른 적절한 페이지로 리다이렉트

def logout_view(request):
    logout(request)
    return redirect('home')


def student_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'student_id' not in request.session:
            messages.error(request, '로그인이 필요합니다.')
            return redirect('student_login')
        return view_func(request, *args, **kwargs)
    return wrapper

@student_login_required
def student_profile(request):
    student = get_object_or_404(Student, student_id=request.session['student_id'])
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            profile = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                profile.set_password(password)
            profile.save()
            messages.success(request, '프로필이 업데이트되었습니다.')
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'student_profile.html', {'form': form})
@student_login_required
def student_activities(request):
    student = Student.objects.get(student_id=request.session['student_id'])
    events = ReligiousEvent.objects.all()
    reserved_events = ReligiousEvent.objects.filter(eventattendance__student=student, eventattendance__reservation='예약')
    return render(request, 'student_activities.html', {
        'events': events,
        'reserved_events': reserved_events
    })

@student_login_required
def student_reservation(request):
    if request.method == 'POST':
        student = Student.objects.get(student_id=request.session['student_id'])
        event_id = request.POST.get('event_id')
        action = request.POST.get('action')
        event = get_object_or_404(ReligiousEvent, event_id=event_id)

        attendance, created = EventAttendance.objects.get_or_create(student=student, event=event)

        if action == 'reserve':
            attendance.reservation = '예약'
            attendance.save()
            messages.success(request, '행사가 예약되었습니다.')
        elif action == 'cancel':
            attendance.reservation = '취소'
            attendance.save()
            messages.success(request, '예약이 취소되었습니다.')

    return redirect('student_activities')

def admin_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not isinstance(request.user, MyAdmin):
            messages.error(request, '관리자 로그인이 필요합니다.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper
@admin_login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@admin_login_required
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

@admin_login_required
def admin_student_activities(request):
    attendances = EventAttendance.objects.select_related('student', 'event').all()
    return render(request, 'admin_student_activities.html', {'attendances': attendances})
# ... (기존 코드 유지)

@admin_login_required
def admin_student_profiles(request):
    search_performed = False
    student = None
    activities = None
    if 'student_id' in request.GET:
        search_performed = True
        student_id = request.GET.get('student_id')
        student = Student.objects.filter(student_id=student_id).first()
        if student:
            activities = EventAttendance.objects.filter(student=student).select_related('event')
    return render(request, 'admin_student_profiles.html', {
        'student': student,
        'activities': activities,
        'search_performed': search_performed
    })
def student_reservation(request):
    student_id = request.session.get('student_id')
    if student_id:
        student = get_object_or_404(Student, student_id=student_id)
        if request.method == 'POST':
            event_id = request.POST.get('event_id')
            event = get_object_or_404(ReligiousEvent, event_id=event_id)  # 여기를 수정
            attendance, created = EventAttendance.objects.get_or_create(student=student, event=event)
            if created:
                messages.success(request, '예약이 완료되었습니다.')
            else:
                if attendance.reservation == '예약':
                    attendance.reservation = '취소'
                    attendance.save()
                    messages.success(request, '예약이 취소되었습니다.')
                else:
                    attendance.reservation = '예약'
                    attendance.save()
                    messages.success(request, '예약이 다시 완료되었습니다.')
            return redirect('student_activities')
        else:
            events = ReligiousEvent.objects.filter(status='예약')
            return render(request, 'student_reservation.html', {'events': events})
    else:
        messages.error(request, '로그인이 필요합니다.')
        return redirect('student_login')
@user_passes_test(lambda u: isinstance(u, MyAdmin))
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

@user_passes_test(lambda u: isinstance(u, MyAdmin))
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

@user_passes_test(lambda u: isinstance(u, MyAdmin))
def admin_event_delete(request, event_id):
    event = get_object_or_404(ReligiousEvent, event_id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, '종교행사가 삭제되었습니다.')
        return redirect('admin_events')
    return render(request, 'admin_event_delete.html', {'event': event})

@user_passes_test(lambda u: isinstance(u, MyAdmin))
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
