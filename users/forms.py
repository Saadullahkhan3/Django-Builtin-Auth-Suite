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
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

"""
Sign UP(User Registration Form, just for context)[Browser shows the emails for auto complete]
<input type="email" name="email" maxlength="254" autofocus="" class="form-control" placeholder="Email address" required="" aria-describedby="id_email_helptext" id="id_email">

Your given(EmailAuthentication form inherited from AuthenticationForm)[Browser NOT shows the emails for auto complete]
<input type="email" name="username" class="form-control" placeholder="Email address" autocomplete="email" autofocus="" maxlength="254" required="" id="id_username">

Full Custom(copy pasted full code of AuthenticationForm with change of username to email)[Browser NOT shows the emails for auto complete]
<input type="email" name="email" class="form-control" placeholder="Email address" autocomplete="email" autofocus="" maxlength="254" required="" id="id_email">
"""

class EmailAuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    email/password logins.
    """
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address',
            'autocomplete': 'email',
            'autofocus': True,
            "name": "email",
        })
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(email)s and password."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.email_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields["email"].label is None:
            self.fields["email"].label = "Email"

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"email": self.email_field.verbose_name},
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
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserPasswordUpdateForm(PasswordChangeForm):
    class Meta:
        model = UserModel
        fields = ("new_password1", "new_password2")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserPasswordResetForm(PasswordResetForm):
    class Meta:
        model = UserModel
        fields = "__all__"
        # fields = ("email",)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


