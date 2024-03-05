from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account successfully created for {username}")
            return redirect('app-home')
    else:
        form = UserRegisterForm()

    return render(request, 'user-templates/register.html', context={'form': form})