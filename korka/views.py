from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ApplicationForm, LoginForm, FeedbackForm
from .models import Application

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get('full_name', '')
            phone = form.cleaned_data.get('phone', '')
            if full_name:  
                names = full_name.split(' ', 2)
                user.first_name = names[0] if len(names) > 0 else ''
                user.last_name = names[1] if len(names) > 1 else ''
            
            user.email = form.cleaned_data.get('email', '')
            user.save()
            messages.success(request, "Регистрация успешна! Теперь вы можете войти в систему.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('applications_list')
    
    form = LoginForm(request.POST or None)
    message = ''
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect('applications_list') 
        else:
            message = 'Неверный логин или пароль'
    return render(request, 'registration/login.html', {'form': form, 'message': message})

@login_required
def applications_list(request):
    apps = Application.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'korka/applications_list.html', {'applications': apps})
    
@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request, "Заявка успешно создана!")
            return redirect('applications_list')
    else:
        form = ApplicationForm()
    return render(request, 'korka/application_create.html', {'form': form})

@login_required
def add_feedback(request, app_id):
    application = get_object_or_404(Application, id=app_id, user=request.user)
    if application.status != 'done':
        messages.error(request, "Вы можете оставить отзыв только после завершения обучения.")
        return redirect('applications_list')

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш отзыв добавлен!")
            return redirect('applications_list')
    else:
        form = FeedbackForm(instance=application)

    return render(request, 'korka/add_feedback.html', {'form': form, 'application': application})