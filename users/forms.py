from email.policy import default
from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm, 
    UserModel, 
    PasswordChangeForm, 
    PasswordResetForm,
)
from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()

"""
Sign UP(User Registration Form, just for context)[Browser shows the emails for auto complete]
<input type="email" name="email" maxlength="254" autofocus="" class="form-control" placeholder="Email address" required="" aria-describedby="id_email_helptext" id="id_email">

Your given(EmailAuthentication form inherited from AuthenticationForm)[Browser NOT shows the emails for auto complete]
<input type="email" name="username" class="form-control" placeholder="Email address" autocomplete="email" autofocus="" maxlength="254" required="" id="id_username">

Full Custom(copy pasted full code of AuthenticationForm with change of username to email)[Browser NOT shows the emails for auto complete]
<input type="email" name="email" class="form-control" placeholder="Email address" autocomplete="email" autofocus="" maxlength="254" required="" id="id_email">
"""

class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        # Field name must stay "username" so LoginView and ModelBackend work.
        # Use EmailInput for UX; keep autocomplete="username" for password managers.
        self.fields["username"].widget = forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email address",
                "autocomplete": "username",
                "autofocus": True,
            }
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "current-password"}
        )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("first_name", "last_name", "username", "email", "bio", "password1", "password2")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ("first_name", "last_name", "username", "bio")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserDelete(forms.Form):
    delete_confirm = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'