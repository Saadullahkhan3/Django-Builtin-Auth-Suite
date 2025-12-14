from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailAuthenticationForm

urlpatterns = [
    path("@<str:username>/", views.UserProfileView.as_view(), name="user_profile"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("update/", views.UserUpdateView.as_view(), name="user_update"),
    path("delete/", views.UserDeleteView.as_view(), name="user_delete"),

    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=EmailAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password/change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html',
        success_url=reverse_lazy('password_change_done'),
    ), name='password_change'),

    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),



    # --- COMPLETE PASSWORD RESET FLOW ---

    # 1. Password Reset Request (user enters email)
    path('password/reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url=reverse_lazy("password_reset_done") # URL to redirect to after email is sent
    ), name='password_reset'),

    # 2. "Done" page shown after email is sent
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    # 3. The link from the email, where user enters a new password
    path('password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url=reverse_lazy("password_reset_complete") # URL to redirect to after successful reset
    ), name='password_reset_confirm'),

    # 4. "Complete" page shown after password has been successfully reset
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    path("", views.UsersList.as_view(), name="users"),
]
