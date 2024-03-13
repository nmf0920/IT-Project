from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from friends.models import Fren
from django.contrib.auth.models import User

# Create your views here.
@login_required
def messageWindow(request):
    user = request.user
    f = Fren.objects.filter(username=user).values()

    return render(request, 'message-templates/messageWindow.html', context={'friends': f})

@login_required
def message(request):
    f = request.GET.get('friendname')
    friend = User.objects.filter(username=f).first()
    user = request.user

    messageDetails = {
        'sender': user, 
        'receiver': friend,
        }

    return render(request, 'message-templates/message.html', context={'messageDetails': messageDetails})