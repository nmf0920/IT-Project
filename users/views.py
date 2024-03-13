from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserPasswordResetForm
from django.contrib.auth.forms import PasswordResetForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.add_message(request, messages.SUCCESS, f"Account successfully created for {username}! You can now login")
            return redirect('user-login')
    else:
        form = UserRegisterForm()

    return render(request, 'user-templates/register.html', context={'form': form})

def password_reset(request):
    if request.method == 'POST':
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password has been changed successfully')
            return redirect('user-login')
        else:
            for field in form:
                for error in field.errors:
                    messages.add_message(request, messages.ERROR, error)
    else:
        form = UserPasswordResetForm()
    return render(request, 'user-templates/password_reset.html', {'form': form})