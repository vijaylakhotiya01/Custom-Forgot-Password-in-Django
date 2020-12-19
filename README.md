# Custom-Forgot-Password-in-Django
Custom Forgot Password Functionality in Django Admin Site

## AIM:
As for now Django Admin Site does not provide to reset password without login or when we forget the Current Password.

This Doc will make you understand how can you set up your Django application with **Forgot Password** module.

### Prerequisite:
1. Python>=3.6
2. Django==3.1.4
3. django-crispy-forms==1.10.0

### minimum required Setup
1. Template Directory
2. Database configure
3. SMTP configure

### Steps to complete the setup:
* First create a view for login which will start the custom forgot password flow.
    1. In template directory create file named:
    `core/templates/admin/accounts/login_temp.html`
       
        Put the login view here.
        ```
        {% extends 'admin/login.html' %}
        {% block content %}
        {{ block.super }}
        <a href="/core/password_reset/"> Forgot Password</a>
        {% endblock %}
       ```
    2. Add this template in admin site for login view.
        
        `core/admin.py`
        ```
        from django.contrib import admin
        admin.site.login_template = "admin/accounts/login_temp.html"
        ```
        Now you will see the Forgot password link in your Django login site.
        As shown in Image.
       
    3. Now add password reset functionality and all other templates of it.
        
        `core/urls.py`
        ```
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
        ```
       
        `core/views.py`
        ```buildoutcfg
        from django.conf import settings
        from django.contrib.auth.forms import PasswordResetForm
        from django.contrib.auth.models import User
        from django.contrib.auth.tokens import default_token_generator
        from django.core.mail import BadHeaderError, send_mail
        from django.db.models import Q
        from django.shortcuts import render, redirect
        from django.http import HttpResponse
        from django.template.loader import render_to_string
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode
        
        
        def password_reset_request(request):
            if request.method == "POST":
                domain = request.headers['Host']
                password_reset_form = PasswordResetForm(request.POST)
                if password_reset_form.is_valid():
                    data = password_reset_form.cleaned_data['email']
                    associated_users = User.objects.filter(Q(email=data))
                    # You can use more than one way like this for resetting the password.
                    # ...filter(Q(email=data) | Q(username=data))
                    # but with this you may need to change the password_reset form as well.
                    if associated_users.exists():
                        for user in associated_users:
                            subject = "Password Reset Requested"
                            email_template_name = "admin/accounts/password/password_reset_email.txt"
                            c = {
                                "email": user.email,
                                'domain': domain,
                                'site_name': 'Interface',
                                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                "user": user,
                                'token': default_token_generator.make_token(user),
                                'protocol': 'http',
                            }
                            email = render_to_string(email_template_name, c)
                            try:
                                send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                            except BadHeaderError:
                                return HttpResponse('Invalid header found.')
                            return redirect("/core/password_reset/done/")
            password_reset_form = PasswordResetForm()
            return render(request=request, template_name="admin/accounts/password/password_reset.html",
                          context={"password_reset_form": password_reset_form})
        ```

    Other Templates:
    `core/templates/admin/accounts/password/password_reset.html`
    ```
    {% extends 'admin/base_site.html' %}
    {% block content %}
        {% load crispy_forms_tags %}
        <!--Reset Password-->
        <div class="container p-5">
            <h2 class="font-weight-bold mt-3">Reset Password</h2>
            <hr>
            <p>Forgotten your password? Enter your email address below, and we'll email instructions for setting a new one.</p>
            <form method="POST">
                {% csrf_token %}
                {{ password_reset_form|crispy }}
                <button class="btn btn-primary" type="submit">Send email</button>
            </form>
        </div>
    {% endblock %}

    ```

    `core/templates/admin/accounts/password/password_reset_complete.html`
    ```
    {% extends 'admin/base_site.html' %}
    {% block content %}
      <!--Password Reset Complete-->
        <div class="container p-4">
    <!--	    <h2 class="font-weight-bold mt-3">Password reset complete</h2>-->
            <hr>
            <p>Your password has been set. You may go ahead and log in now.</p>                 
            <a href="/admin/" class="btn btn-primary">Log in</a>
        </div>
    {% endblock %}
    ```
    
    `core/templates/admin/accounts/password/password_reset_confirm.html`
    ```
    {% extends 'admin/base_site.html' %}
    {% block content %}
    {% load crispy_forms_tags %}
    <!--Password Reset Confirm-->
    <div class="container p-5">
	    <h2 class="font-weight-bold mt-3">Password Reset Confirm</h2>
		<hr>
        <p>Please enter your new password.</p>
        <form method="POST">
            {% csrf_token %}
            {{ form|crispy }}                    
            <button class="btn btn-primary" type="submit">Reset password</button>
        </form>
    </div>
    {% endblock %}
    ```
  
    `core/templates/admin/accounts/password/password_reset_done.html`
    ```
    {% extends 'admin/base_site.html' %}
    {% block content %}
    {% load crispy_forms_tags %}
    <!--Password Reset Confirm-->
    <div class="container p-5">
	    <h2 class="font-weight-bold mt-3">Password Reset Confirm</h2>
		<hr>
        <p>Please enter your new password.</p>
        <form method="POST">
            {% csrf_token %}
            {{ form|crispy }}                    
            <button class="btn btn-primary" type="submit">Reset password</button>
        </form>
    </div>
    {% endblock %}
    ```
  
    `core/templates/admin/accounts/password/password_reset_email.txt`
    ```
    {% autoescape off %}
    Hello,
    We received a request to reset the password for your account for this email address. To initiate the password reset process for your account, click the link below.
    {{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
    This link can only be used once. If you need to reset your password again, please request another reset.
    If you did not make this request, you can ignore this email.
    
    Sincerely,
    The XYZ Team
    {% endautoescape %}
    ```
    

