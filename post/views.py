from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from postman.models import Message as PostmanMessage
from postman.models import MessageManager
from postman.views import WriteView, InboxView
from postman.api import pm_write
from django.shortcuts import HttpResponse
from friends.models import Fren
from django.db.models import Max
from django.db.models import Subquery, OuterRef
from itertools import groupby

@login_required
def inbox(request):
    user = request.user
    inbox_messages = PostmanMessage.objects.inbox(user)

    # Annotate each message with the sender's username
    annotated_messages = inbox_messages.annotate(
        sender_username=Subquery(
            User.objects.filter(pk=OuterRef('sender_id')).values('username')[:1]
        )
    )

    # Group the messages by the sender's username
    grouped_messages = annotated_messages.order_by('sender_username').values('sender_username', 'body', 'sent_at')

    # Convert the grouped messages to a dictionary for easier access
    grouped_dict = {
        sender: max(messages, key=lambda x: x['sent_at'])
        for sender, messages in groupby(grouped_messages, key=lambda x: x['sender_username'])
    }

    return render(request, 'post-templates/inbox.html', {'latest_messages': grouped_dict})
    # try:
    #     u = request.user
    #     user = User.objects.get(username=u)
    #     inbox = PostmanMessage.objects.inbox(user)
    # except User.DoesNotExist:
    #     return HttpResponse("No such user")

    # return render(request, 'post-templates/inbox.html', context={'inbox': inbox})

@login_required
def view_message(request, message_id):
    # message_manager = MessageManager()
    message = get_object_or_404(PostmanMessage, id=message_id)
    if message.recipient != request.user:
        return redirect('message-inbox')

    # thread = message_manager.thread_for(request.user, message.sender)
    message.read_at = None
    message.save()
    return render(request, 'post-templates/view_message.html', {'message': message})

@login_required
def compose(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient', None)
        re = User.objects.get(username=recipient_username)
        recipient = get_object_or_404(User, username=re)
        body = request.POST.get('body')
        pm_write(
            sender = request.user,
            recipient = recipient,
            subject=body[:50],
            body = body,
        )
        return redirect('message-inbox')
    mainuser = User.objects.get(username=request.user)
    users = Fren.objects.filter(username=mainuser).values()
    return render(request, 'post-templates/compose.html', {'users': users})

@login_required
def message_thread(request, message_sender):
    sender = request.user
    receiver = User.objects.get(username=message_sender)

    sent_by_sender = PostmanMessage.objects.filter(sender=sender, recipient=receiver)
    sent_by_receiver = PostmanMessage.objects.filter(sender=receiver, recipient=sender)

    message_thread = sent_by_sender | sent_by_receiver
    message_thread.order_by('sent_at')

    return render(request, 'post-templates/message_thread.html', {'message_thread': message_thread})