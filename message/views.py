from django.shortcuts import render, redirect
from friends.models import Fren

# Create your views here.
def messageWindow(request):
    user = request.user
    f = Fren.objects.filter(username=user).all()

    return render(request, 'message-templates/messageWindow.html', context={'friends': f})