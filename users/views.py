from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, get_user_model
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin 

from .forms import (
    UserDelete,
    UserRegistrationForm, 
    UserUpdateForm,
)
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pprint import pprint

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
UserModel = get_user_model()
class UsersList(ListView):
    model = UserModel
    template_name = "users/users.html"
    context_object_name = "users"


# def user_profile(request, username):
#     profile = get_object_or_404(UserModel, username=username)
#     return render(request, "registration/user_profile.html", {"profile": profile})
class UserProfileView(DetailView):
    model = UserModel
    template_name = 'registration/user_profile.html'
    context_object_name = 'profile'
    slug_field = 'username__iexact' # Use a case-insensitive lookup
    slug_url_kwarg = 'username'

# def user_register(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             # user = form.save(commit=False)
#             user = form.save()
#             # user.set_password(form.cleaned_data["password1"])
#             login(request, user)
#             return redirect('user_profile', username=request.user.username)
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'registration/register.html', {"form": form}) 
class UserRegisterView(SuccessMessageMixin, CreateView):
    """Replaces the user_register function."""
    model = UserModel
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_message = "Your profile has been created successfully."

    def get_success_url(self):
        # Redirect to the new user's profile page
        return reverse_lazy('user_profile', kwargs={'username': self.object.username})

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save()
        login(self.request, user) # Log the user in automatically
        return super().form_valid(form)

# @login_required
# def user_update(request):
    # if request.method == "POST":
    #     form = UserUpdateForm(request.POST, instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('user_profile', username=request.user.username)
    # else:
    #     form = UserUpdateForm(instance=request.user)
    # return render(request, 'registration/user_update.html', {"form": form})
class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Replaces the user_update function."""
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'registration/user_update.html'
    success_message = "Your profile has been updated successfully."

    def get_success_url(self):
        # Redirect to the user's own profile page after update
        return reverse_lazy('user_profile', kwargs={'username': self.request.user.username})

    def get_object(self, queryset=None):
        # Ensures that users can only edit their own profile
        return self.request.user


# @login_required
# def user_delete(request):
#     if request.method == "POST":
#         form = UserDelete(request.POST)
#         if form.is_valid():
#             redirect_link = request.META.get("HTTP_REFERER") or "home"
#             if form.cleaned_data.get("delete_confirm", None):
#                 # request.user.is_active = False # Soft delete

#                 # request.user.delete()
#                 logout(request) 
#                 return redirect("home")
#             return redirect(redirect_link)
            
#     else:
#         form = UserDelete()
#     return render(request, 'registration/user_delete.html', {"user": request.user, "form": form}) 
    
class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Replaces the user_delete function."""
    model = UserModel
    template_name = 'registration/user_delete.html'
    success_url = reverse_lazy('home')
    form_class = UserDelete 
    success_message = "Your account has been successfully deleted."

    def get_object(self, queryset=None):
        # Ensures that users can only delete their own profile
        return self.request.user

    def form_valid(self, form):
        # The form from get_form() is passed in.
        # We need to check our custom 'delete_confirm' field.
        if form.cleaned_data.get("delete_confirm"):
            return super().form_valid(form)
        else:
            # If checkbox isn't checked, re-render the form with an error.
            form.add_error("delete_confirm", "You must check this box to confirm deletion.")
            return self.form_invalid(form)