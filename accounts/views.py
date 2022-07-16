import django.utils.http
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Accounts
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.

def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        # user = Accounts.objects.filter(email=email, password=password).exists()
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "User Logged in Successfully")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials. Please Try Again.")
            return redirect('signin')

    return render(request, 'accounts/signin.html')


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            phone_number = form.cleaned_data['phone_number']
            username = form.cleaned_data['username']
            user = Accounts.objects.create_account(
                full_name=full_name,
                email=email,
                password=password,
                username=username,
            )
            user.phone_number = phone_number
            user.save()
            # email verification
            current_site = get_current_site(request)
            mail_subject = "Please activate your account."
            message = render_to_string('accounts/mail_message_verification.html', dict(
                user=user,
                domain=current_site,
                uid=urlsafe_base64_encode(force_bytes(user.pk)),
                token=default_token_generator.make_token(user),
            ))
            mail = email
            send_mail = EmailMessage(mail_subject, message, to=[mail, ])
            send_mail.send()
            # messages.success(request, 'An email was sent for verification. Kindly click on that link to activate your account.')
            return redirect('/accounts/signin/?command=verification&email=' + email)

    else:
        form = RegistrationForm()
    data = dict(
        form=form,
    )
    return render(request, 'accounts/register.html', data)


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are successfully logged out.")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk=uid)
        print(uid, user.full_name)
    except(TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
        user = None
    print(uid, user.full_name)
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is successfully activated. Please login with credentials.")
        return redirect('signin')
    else:
        messages.error(request, "Invalid activation link.")
        return redirect('register')
