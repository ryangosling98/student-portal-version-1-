# student-portal-version-1-


 

Let's call our project "StudentPortal". Here's a step-by-step guide:



```python
# Step 1: Set up the Django project

1. Open a terminal and create a new Django project:
   ```
   django-admin startproject StudentPortal
   cd StudentPortal
   python manage.py startapp portal
   ```

2. Add 'portal' to INSTALLED_APPS in StudentPortal/settings.py:
   ```python
   INSTALLED_APPS = [
       ...
       'portal',
   ]
   ```

# Step 2: Create the registration form

3. In portal/forms.py:
```python
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
```

# Step 3: Create a custom model

4. In portal/models.py:
```python
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True)
    major = models.CharField(max_length=100)
    gpa = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"
```

# Step 4: Set up admin for the model

5. In portal/admin.py:
```python
from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'major', 'gpa')
    search_fields = ('user__username', 'student_id', 'major')
```

# Step 5: Create views for registration and profile creation

6. In portal/views.py:
```python
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
```

# Step 6: Set up URLs

7. In StudentPortal/urls.py:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
]
```

8. Create portal/urls.py:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('profile/', views.profile, name='profile'),
]
```

# Step 7: Create templates

9. Create templates in portal/templates/portal/:

register.html:
```html
<h2>Register</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Register</button>
</form>
```

create_profile.html:
```html
<h2>Create Student Profile</h2>
<form method="post">
    {% csrf_token %}
    <label for="student_id">Student ID:</label>
    <input type="text" name="student_id" required>
    <label for="major">Major:</label>
    <input type="text" name="major" required>
    <label for="gpa">GPA:</label>
    <input type="number" name="gpa" step="0.01">
    <button type="submit">Create Profile</button>
</form>
```

profile.html:
```html
<h2>Student Profile</h2>
<p>Username: {{ profile.user.username }}</p>
<p>Student ID: {{ profile.student_id }}</p>
<p>Major: {{ profile.major }}</p>
<p>GPA: {{ profile.gpa }}</p>
```

# Step 8: Database setup and connectivity check

10. In StudentPortal/settings.py, ensure the database settings are correct:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

11. Create a management command to check database connectivity. 
    Create a new file portal/management/commands/check_db.py:

```python
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    help = 'Checks database connectivity'

    def handle(self, *args, **options):
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
        except OperationalError:
            self.stdout.write(self.style.ERROR('Database unavailable'))
        else:
            self.stdout.write(self.style.SUCCESS('Database connection successful'))
```

# Step 9: Run migrations and create superuser

12. Run the following commands:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

# Step 10: Test database connectivity

13. Run the custom management command:
```
python manage.py check_db
```

# Step 11: Run the server

14. Start the development server:
```
python manage.py runserver
```

```

