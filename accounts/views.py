from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm  # AuthenticationForm'u import edin
from .forms import RegisterForm
from .models import Profile


User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('merhaba')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def home_view(request):
    return render(request, 'accounts/home.html', {'user': request.user})

def home(request):
    return render(request, 'accounts/home.html', {'user': request.user})

def merhaba(request):
    return render(request, 'accounts/merhaba.html')

def send_reset_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            code = get_random_string(length=6, allowed_chars='0123456789')
            user.profile.reset_code = code
            user.profile.save()
            send_mail(
                'Şifre Sıfırlama Kodu',
                f'Şifre sıfırlama kodunuz: {code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Şifre sıfırlama kodu e-posta adresinize gönderildi.')
            return redirect('verify_code')
    return render(request, 'accounts/password_reset.html')

def verify_code(request):
    if request.method == 'POST':
        code = request.POST['code']
        user = User.objects.filter(profile__reset_code=code).first()
        if user:
            return redirect(reverse('password_reset_confirm', kwargs={'uidb64': user.pk, 'token': code}))
        else:
            messages.error(request, 'Geçersiz kod.')
    return render(request, 'accounts/verify_code.html')

def password_reset_confirm(request, uidb64, token):
    user = User.objects.get(pk=uidb64)
    if user.profile.reset_code == token:
        if request.method == 'POST':
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.profile.reset_code = ''
            user.profile.save()
            user.save()
            messages.success(request, 'Şifreniz başarıyla güncellendi.')
            return redirect('login')
        return render(request, 'accounts/password_reset_confirm.html')
    else:
        return HttpResponse('Geçersiz kod.', status=400)