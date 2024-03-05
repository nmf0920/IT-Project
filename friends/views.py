from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from .models import Fren
from django.contrib import messages

def addfriends(request):
    if request.method == 'POST':
        name = request.POST.get('friendname', None)

        try:
            friend = User.objects.get(username=name)
            user = User.objects.get(username=request.user)

            friend1 = Fren(username=user, friendname=friend)
            friend2 = Fren(username=friend, friendname=user)

            friend1.save()
            friend2.save()

            messages.add_message(request, messages.SUCCESS, f'Successfully added {friend} as your friend!')

            return redirect('add-friend')
        except User.DoesNotExist:
            return HttpResponse("No such user")

    return render(request, 'friends-templates/addfriend.html')

# def makefriends(request):
#     if request.method == 'POST':
