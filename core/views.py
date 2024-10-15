"""
Core views
"""

from core.auth.email.contactus import ContactUsView
from core.auth.email.email_verification import (EmailVerificationView,
                                                RequestEmailVerificationView)
from core.auth.login import LoginView
from core.auth.logout import LogOutView
from core.auth.password.password_change import PasswordChangeView
from core.auth.password.password_reset import (PasswordResetCompleteView,
                                               PasswordResetConfirmView,
                                               PasswordResetDoneView,
                                               RequestPasswordResetView)
from core.auth.signup import SignupView
from core.auth.socialAuth import (GoogleAuthenticationCallbackView,
                                  GoogleAuthenticationView)
from core.users.delete import AccountDeletionView
from core.users.details import UserUpdateView

google_authentication_view = GoogleAuthenticationView.as_view()
google_authentication_callback_view = (
    GoogleAuthenticationCallbackView.as_view()
)
login_view = LoginView.as_view()
logout_view = LogOutView.as_view()
signup_view = SignupView.as_view()
email_verification_view = EmailVerificationView.as_view()
request_email_verification_view = RequestEmailVerificationView.as_view()

password_change_view = PasswordChangeView.as_view()
request_password_reset_view = RequestPasswordResetView.as_view()
password_reset_done_view = PasswordResetDoneView.as_view()
password_reset_confirm_view = PasswordResetConfirmView.as_view()
password_reset_complete_view = PasswordResetCompleteView.as_view()

contactus_view = ContactUsView.as_view()

user_update_view = UserUpdateView.as_view()
user_account_deletion_view = AccountDeletionView.as_view()
