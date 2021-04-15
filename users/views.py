from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import logout, authenticate, login

# Create your views here.\
from django.urls import reverse

from users.form import SignInForm, SignUpForm
from users.models import Profile


def log_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST':
        form = SignInForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active and user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))

            else:
                profile = Profile.objects.get(pk=user.id)
                # import pdb;pdb.set_trace()
                if user.is_active and profile and profile.is_authorized:
                    login(request, user)
                    return HttpResponseRedirect(reverse('dashboard'))
                else:
                    messages.warning(request,
                                     'Your account is inactive. ')
        else:
            messages.warning(request, 'Invalid login details given.')

    form = SignInForm()
    return render(request, 'index.html', {'form': form})


def dashboard(request):
    if request.user.is_authenticated:

        return render(request, 'dashboard/dashboard.html', {})
    else:
        return HttpResponseRedirect(reverse('login'))

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def sign_up(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            messages.warning(request,
                             'Your information is incorrect.')

    return render(request, 'signup.html', {'form': form})


def profile(request):
    return render(request, 'dashboard/profile.html', {})
