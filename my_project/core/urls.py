from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/', views.index),
    # path('accounts/', include('django.contrib.auth.urls')),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="admin/accounts/password/password_reset_confirm.html"), name='password_reset_confirm'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='admin/accounts/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='admin/accounts/password/password_reset_complete.html'), name='password_reset_complete'),
]