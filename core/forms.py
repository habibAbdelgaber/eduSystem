from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import \
    PasswordChangeForm as BasePasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import forms as auth_forms

from .models import UserProfile

class UserChangeForm(auth_forms.UserChangeForm):
    """
    User change form
    """
    first_name = forms.CharField(label=_(''), max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control py-2', 'placeholder': 'First Name', 'autofocus': True}))
    last_name = forms.CharField(label=_(''), max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control py-2', 'placeholder': 'Last Name', 'autofocus': True}))
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')
        exclude = ('password',)

class UserProfileForm(forms.ModelForm):
    """
    User profile form
    """
    bio = forms.CharField(label=_(''), max_length=250, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio', 'autofocus': True, 'rows': '3', 'resize': '0', 'cols': '50'}))
    class Meta:
        model = UserProfile
        fields = ('bio', 'img')


class SignupForm(forms.ModelForm):
    """
    Signup form
    """

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control py-2',
                'placeholder': 'Email address',
            }
        ),
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control py-2',
                'placeholder': 'Create Password',
            }
        ),
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control py-2',
                'placeholder': 'Confirm Password',
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']

    def clean(self, *args, **kwargs):
        """
        Check if email is already registered, password mismatch, and password is at least 8 characters long
        """
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if email and password2 and password2:
            if get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError(_('Email is already in use.'))

            if password1 != password2:
                raise forms.ValidationError(_('Passwords do not match'))
            if len(str(password1)) < 8:
                raise forms.ValidationError(
                    'Password must be at least 8 characters long'
                )

        return super().clean(*args, **kwargs)

    def save(self, commit=True):
        """
        Create user and save it
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    """
    Login form
    """

    username = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control py-2',
                'placeholder': 'Username or Email address',
            }
        ),
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control py-2', 'placeholder': 'Password'}
        ),
    )
    """
    Custom Login Form
    """

    def clean(self):
        """
        Check if user is authenticated, password is correct,
        and user's account is not disabled or deleted,
        and is user's account is inactive
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(
                    _('an invalid username or password')
                )

            if not user.is_active:
                raise forms.ValidationError(_('Your account is inactive'))

            if not user.is_authenticated:
                raise forms.ValidationError(_('Invalid username or password'))

        return super().clean()

class EmailVerificationResendForm(forms.Form):
    """
    Email verification resend form
    """

    email = forms.EmailField(
        label=(''),
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control py-2',
                'placeholder': 'Email address',
            }
        ),
    )

    def clean(self):
        """
        Check if email is registered
        """
        email = self.cleaned_data.get('email')
        if not get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(_('Email is not registered'))

        return self.cleaned_data

class PasswordChangeForm(BasePasswordChangeForm):
    """
    Password change form
    """

    old_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control py-2', 'placeholder': 'Old Password'}
        ),
    )
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control py-2', 'placeholder': 'New Password'}
        ),
    )
    new_password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control py-2',
                'placeholder': 'Confirm New Password',
            }
        ),
    )

    def clean(self):
        """
        Check if user is authenticated, password is correct,
        and user's account is not disabled or deleted,
        and if user's account is not inactive.
        """
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 != new_password2:
            raise forms.ValidationError(_('Passwords do not match'))
        if len(str(new_password1)) < 8:
            raise forms.ValidationError(
                _('Password must be at least 8 characters long')
            )

        return self.cleaned_data

class RequestPasswordResetForm(PasswordResetForm):
    """
    Password reset form
    """

    email = forms.EmailField(
        label=(''),
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control py-2',
                'placeholder': 'Email address',
            }
        ),
    )

    def clean(self):
        """
        Check if email is registered and the user is not disabled or inactive
        """
        email = self.cleaned_data.get('email')
        if not get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(_('Email does not exist'))
            # return redirect('core:login')
        if get_user_model().objects.filter(email=email).exists():
            user = get_user_model().objects.get(email=email)
            if not user.is_active:
                raise forms.ValidationError(
                    _(
                        'Your account is inactive. Make sure you have activated your account.'
                    )
                )
        return self.cleaned_data

class SetPasswordForm(BaseSetPasswordForm):
    """
    Set password form
    """

    new_password1 = forms.CharField(
        label=_(''),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control py-2', 'placeholder': 'New Password'}
        ),
    )
    new_password2 = forms.CharField(
        label=_(''),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control py-2',
                'placeholder': 'Confirm Password',
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

    # def __init__(self, *args, **kwargs):

    #     # self.user = kwargs.pop('user', None)
    #     super().__init__(*args, **kwargs)

    def clean(self):
        """
        Check if passwords match
        """
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 != password2:
            raise forms.ValidationError(_('Passwords do not match'))

        if len(str(password1)) < 8:
            raise forms.ValidationError(
                _('Password must be at least 8 characters long')
            )

        return self.cleaned_data

class ContactUsForm(forms.Form):
    """
    Contact us form
    """

    name = forms.CharField(
        label=_(''),
        widget=forms.TextInput(
            attrs={'class': 'form-control py-2', 'placeholder': 'Your Name'}
        ),
    )
    email = forms.EmailField(
        label=_(''),
        widget=forms.EmailInput(
            attrs={'class': 'form-control py-2', 'placeholder': 'Your Email'}
        ),
    )
    subject = forms.CharField(
        label=_(''),
        widget=forms.TextInput(
            attrs={'class': 'form-control py-2', 'placeholder': 'Subject'}
        ),
    )
    message = forms.CharField(
        label=_(''),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control py-2',
                'placeholder': 'Your Message',
                'rows': '5',
                'cols': '30',
                'style': 'resize: none',
            }
        ),
    )
