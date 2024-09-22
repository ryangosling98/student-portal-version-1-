from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from .models import StudentProfile


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('create_profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'portal/register.html', {'form': form})


def create_profile(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        major = request.POST.get('major')
        gpa = request.POST.get('gpa')

        StudentProfile.objects.create(
            user=request.user,
            student_id=student_id,
            major=major,
            gpa=gpa
        )
        return redirect('profile')
    return render(request, 'portal/create_profile.html')


def profile(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    return render(request, 'portal/profile.html', {'profile': student_profile})