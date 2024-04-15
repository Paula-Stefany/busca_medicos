from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from medicSearch.forms.AuthForm import LoginForm, RegisterForm, RecoveryForm, ChangePassordForm
from medicSearch.models.Profile import Profile
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import hashlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def login_view(request):
    loginForm = LoginForm()
    message = None

    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username']  
        password = request.POST['password']
        loginForm = LoginForm(request.POST)

        if loginForm.is_valid():
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                _next = request.GET.get('next')

                if _next is not None:
                    return redirect(_next)
                else:
                    return redirect('/')
            else:
                message = {
                    'type': 'danger',
                    'text': 'Dados de usuário incorretos'
                }
    context = {
        'form': loginForm,
        'message': message,
        'title': 'Login',
        'button_text': 'Entrar', 
        'link_text': 'Registrar',
        'link_href': '/register'
    }

    return render(request, template_name='auth/auth.html', context=context, status=200)

def register_view(request):
    registerForm =RegisterForm()
    message = None 

    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        registerForm = RegisterForm(request.POST)

        if registerForm.is_valid():
            verifyUsername = User.objects.filter(username=username).first()
            verifyEmail = User.objects.filter(email=email).first()

            if verifyUsername is not None:
                message = {'type': 'danger', 'text': 'Já existe um usuário com este username!'}
            
            elif verifyEmail is not None:
                message = {'type': 'danger', 'text': 'Já existe um usuário com esse e-mail!'}
            else:
                user = User.objects.create_user(username, email, password)

                if user is not None:
                    message = {'type': 'success', 'text': 'Conta criada com sucesso'}
                else:
                    message = {'type': 'danger', 'text': 'Um erro ocorreu ao tantar criar o usuário.'}

    context = {
            'form': registerForm,
            'message': message,
            'title': 'Registrar',
            'button_text': 'Registrar',
            'link_text': 'Login',
            'link_href': '/login'
    }
    return render(request, template_name='auth/auth.html', context=context, status=200)

def logout_view(request):
    logout(request)
    return redirect('/login')

def recovery_view(request):
    recoveryForm = RecoveryForm()
    message = None

    if request.method == 'POST':
        recoveryForm = RecoveryForm(request.POST)

        if recoveryForm.is_valid():
            email = request.POST['email']
            profile = Profile.objects.filter(user__email=email).first()

            if profile is not None:
                try:
                    send_email(profile)
                    message = {
                        'type': 'success',
                        'text': 'Um e-mail foi enviado para sua caixa de entrada.'
                    }
                except:
                    message = {'type': 'danger', 'text': 'Erro no envio do email.'}
            else:
                message = {'type': 'danger', 'text': 'E-mail inexistente'}
        else:
            message = {'type': 'danger', 'text': 'Formulário inválido'}

    context = {
        'form': recoveryForm,
        'message': message,
        'title': 'Recuperar senha',
        'button_text': 'Recuperar',
        'link_text': 'Login',
        'link_href': '/login'
    }

    return render(request, template_name='auth/auth.html', context=context, status=200)

def send_email(profile):
    try:

        profile.token = hashlib.sha256().hexdigest()
        profile.save()

        html_message = render_to_string('auth/recovery.html', {'token': profile.token})
        plain_message = strip_tags(html_message)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Recuperação de senha'
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = profile.user.email

        msg.attach(MIMEText(plain_message, 'plain'))
        msg.attach(MIMEText(html_message, 'html'))

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, profile.user.email, msg.as_string())
            print('Email enviado com sucesso!')

            server.quit()
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

def change_password(request, token):
    profile = Profile.objects.filter(token=token).first()
    changePasswordForm = ChangePassordForm()
    message = None 
    link_text = 'Solicitar recuperação de senha'
    link_href = '/recovery'

    if profile is not None:
        if request.method == 'POST':
            changePasswordForm = ChangePassordForm(request.POST)
            if changePasswordForm.is_valid():
                profile.user.set_password(request.POST['password'])
                profile.token = None
                profile.user.save()
                profile.save()
                message = {'type': 'success', 'text': 'Senha alterada com sucesso!!!'}
                link_text = 'Login'
                link_href = '/login'
            else:
                message = {'type': 'danger', 'text': 'Formulário inválido.'}
    else:
        message = {'type': 'danger', 'text': 'Token inválido. Solicite novamente.'}

    context = {
        'form': changePasswordForm,
        'message': message,
        'title': 'Alterar senha',
        'button_text': 'Alterar',
        'link_text': link_text,
        'link_href': link_href
    }
    return render(request, template_name='auth/auth.html', context=context, status=200)
