from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from . import models
from . import forms


def home(request):
    return render(request, 'home.html')


def sign_up(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('home'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('home')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def show_profile(request):
    current_user = request.user
    # this is wierd, but i didn't find any other solution how to do it
    try:
        avatar_picture = "/static"+current_user.avatar.url
    except ValueError:
        avatar_picture = None
    return render(request, 'accounts/profile.html',
    {'current_user': current_user, 'avatar_picture': avatar_picture})


@login_required
def edit_profile(request):
    instance = request.user
    form = forms.EditSignUpForm(instance=instance)
    if request.method == 'POST':
        form = forms.EditSignUpForm(request.POST, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(
            request,
            'Your profile has been successfully edited!'
            )
            return HttpResponseRedirect(reverse('accounts:show_profile'))
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def upload_avatar(request):
    instance = request.user
    form = forms.AvatarUpload(instance=instance)
    if request.method == 'POST':
        form = forms.AvatarUpload(request.POST, request.FILES, instance=instance)
        uploaded_photo = request.FILES['avatar']
        instance.avatar = uploaded_photo
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(
                request,
                "Your avatar has been successfully uploaded!"
            )
            return HttpResponseRedirect(reverse('accounts:show_profile'))
        else:
            messages.error(
                request,
                "Your form is not correct!"
            )
    return render(request, 'accounts/upload_avatar.html', {'form': form})


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid:
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
