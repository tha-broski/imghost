from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm

# Create your views here.

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'You are already logged in')
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                email = form.cleaned_data.get('email').strip().lower()
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=raw_password)
                if account is not None:
                    login(request, account)
                    destination = get_redirect_if_exists(request)
                    if destination:
                        return redirect(destination)
                    return redirect('home')
                else:
                    context['registration_form'] = form
                    context['error'] = 'Authentication failed after registration.'
            except Exception as e:
                context['registration_form'] = form
                context['error'] = f'Registration error: {str(e)}'

    
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect("home")

def login_view(request, *args, **kwargs):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data.get('email').strip().lower()
                password = form.cleaned_data.get('password')
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    destination = get_redirect_if_exists(request)
                    if destination:
                        return redirect(destination)
                    return redirect("home")
                else:
                    context['login_form'] = form
                    context['error'] = 'Invalid credentials.'
            except Exception as e:
                context['login_form'] = form
                context['error'] = f'Login error: {str(e)}'


    return render(request, "account/login.html", context)

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect
