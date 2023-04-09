from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm, PasswordChangeFormLabelUpdate, EmailForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User

# Create your views here.


# w htmlu {% if user.is_authenticated %} jak sprawdzamy czy jest zalogowany.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_user(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        if request.method == "POST":
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                if User.objects.filter(email=email).exists():
                    messages.success(request, ("Ten email jest już zarejestrowany"))
                    return redirect('register_user')
                else:
                    form.save()
                    messages.success(request, ("Zostałeś zarejestrowany"))
                    return redirect('login_user')
        else:
            form = RegisterUserForm()
        return render(request, "authenticate/register_user.html", {
            'form': form,
        })
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.success(request, ("Błędne hasło bądź nazwa użytkownika"))
            return redirect('login_user')
    else:
        return render(request, "authenticate/login.html", {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_page(request):
    return render(request, "authenticate/home.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    messages.success(request, ("Zostałeś wylogowany"))
    return redirect('home_page')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_user')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeFormLabelUpdate(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Hasło zostało zmienione')
            return redirect('profile')
    else:
        form = PasswordChangeFormLabelUpdate(request.user)
    return render(request, 'authenticate/change_password.html', {
        'form': form
    })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_user')
def profile(request):
    return render(request, "authenticate/profile.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_user')
def change_email(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.success(request, ("Taki email już istnieje!"))
                return redirect('change_email')
            else:
                old_email = User.objects.get(email=request.user.email)
                new_email = request.POST['email']
                old_email.email = new_email
                old_email.save()
                print(User.email)
                print(request.user.email)
                messages.success(request, ("Zmieniono email"))
                return redirect('profile')
    else:
        form = EmailForm()
    return render(request, "authenticate/change_email.html", {
        'form': form,
    })

