from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import logout, authenticate, login

# Create your views here.\
from django.urls import reverse

from users.form import SignInForm, SignUpForm
from users.models import Profile
from classes.forms import classForm


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


def change_password(request):
    return render(request, 'dashboard/change_password.html', {})


def class_setup(request):
    return render(request, 'dashboard/class_setup.html', {})


def section_setup(request):
    return render(request, 'dashboard/section_setup.html', {})


def shift_setup(request):
    return render(request, 'dashboard/shift_setup.html', {})


def view_structure(request):
    return render(request, 'dashboard/view_structure.html', {})


def user_profile(request):
    return render(request, 'dashboard/user_profile.html', {})


def fee_structure(request):
    return render(request, 'dashboard/fee_structure.html', {})


def add_fee_category(request):
    return render(request, 'dashboard/add_fee_category.html', {})


def add_class(request):
    form = classForm()
    if request.method == 'POST':
        # print(request.POST)
        form = classForm(request.POST)
        if form.is_valid():
            form.save()
        form.clean()
    context = {'form': form}
    # return render(request, 'dashboard/add_class.html', {})
    return render(request, 'dashboard/add_class.html', context)
