from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserModel
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import (
    EmailAuthenticationForm,
    UserPasswordResetForm,
    UserPasswordUpdateForm, 
    UserRegistrationForm, 
    UserUpdateForm
)

# Create your views here.
'''
Profile:
See
Create
Update
Delete

Password:
Change
Reset
'''
from pprint import pprint

def user_profile(request, username):
    profile = get_object_or_404(UserModel, username=username)
    return render(request, "registration/user_profile.html", {"profile": profile})


def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {"form": form}) 


@login_required
def user_update(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'registration/user_update.html', {"form": form})


@login_required
def user_delete(request):
    if request.method == "POST":
        # For delete, you might want a confirmation form instead
        request.user.delete()
        logout(request)  # Log out the deleted user
        return redirect('home')
    else:
        # Pass user context for confirmation
        pass
    return render(request, 'registration/user_delete.html', {"user": request.user}) 
    

@login_required
def user_password_update(request):
    if request.method == "POST":
        form = UserPasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserPasswordUpdateForm(request.user)
    return render(request, 'registration/password_update.html', {"form": form}) 


def user_password_reset(request):
    if request.method == "POST":
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,  # Needed for email context
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
            )
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserPasswordResetForm()
    return render(request, 'registration/password_reset.html', {"form": form}) 


def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_profile', username=request.user.username)
    else:
        form = EmailAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def confirm_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # or wherever you want to redirect after logout
    return render(request, 'registration/logout.html')
