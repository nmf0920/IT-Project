from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from .models import Fren
from django.contrib import messages

@login_required
def addfriends(request):
    if request.method == 'POST':
        name = request.POST.get('friendname', None)

        try:
            friend = User.objects.get(username=name)
            user = User.objects.get(username=request.user)

            x = Fren.objects.filter(username=user, friendname=friend)
            if not x:
                friend1 = Fren(username=user, friendname=friend)
                friend2 = Fren(username=friend, friendname=user)

                friend1.save()
                friend2.save()

                messages.add_message(request, messages.SUCCESS, f'Successfully added {friend} as your friend!')
            else:
                messages.add_message(request, messages.INFO, f'You  are already friends with {friend}')
            return redirect('add-friend')
        except User.DoesNotExist:
            messages.add_message(request, messages.WARNING, f'No such user exists!')
            return redirect('add-friend')

    return render(request, 'friends-templates/addfriend.html')

# def makefriends(request):
#     if request.method == 'POST':
