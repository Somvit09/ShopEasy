from django.shortcuts import render
from .forms import RegistrationForm
from .models import Accounts
from django import forms

# Create your views here.

def signin(request):
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

    else:
        form = RegistrationForm()
    data = dict(
        form=form,
    )
    return render(request, 'accounts/register.html', data)


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
