"""
Core urls
"""

from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path(
        'google-login/', views.google_authentication_view, name='google-login'
    ),
    path(
        'oauth/callback/',
        views.google_authentication_callback_view,
        name='google-login-callback',
    ),
    path(
        'email-verification/<uidb64>/<token>/',
        views.email_verification_view,
        name='email-verification',
    ),
    path(
        'request-verification/',
        views.request_email_verification_view,
        name='request-verification',
    ),
    # password reset and change
    path(
        'password/change/',
        views.password_change_view,
        name='password-change-view',
    ),
    path(
        'password/reset/',
        views.request_password_reset_view,
        name='password-reset',
    ),
    path(
        'password-reset/done/',
        views.password_reset_done_view,
        name='password-reset-done',
    ),
    path(
        'password-reset/confirm/<uidb64>/<token>/',
        views.password_reset_confirm_view,
        name='password-reset-confirm',
    ),
    path(
        'password-reset/complete/',
        views.password_reset_complete_view,
        name='password-reset-complete',
    ),
    path('contactus/', views.contactus_view, name='contactus'),
    path('user-details/<pk>/', views.user_update_view, name='user-update'),
    path(
        'account-deletion/<pk>/',
        views.user_account_deletion_view,
        name='account-deletion',
    ),
]
