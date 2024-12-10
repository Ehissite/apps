from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm

# Create your views here.
@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    
    if item.created_by == request.user:
        return redirect('core:dashboard')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id]) # conversations the user is a part of
    
    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id) # redirect to conversation page
    
    if request.method == "POST":
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()
            
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            
            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()
    
    return render(request, 'conversation/message.html', {
        'form': form,
        'title':  item.created_by,
        
    })
    
@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])  # all the conversations the user has
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
        'title':  "Send Message",
        
    })

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    
    if request.method == "POST":
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            
            conversation.save()
            
            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm(request.POST)
        
    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'title':  "Conversation",
        'form': form,
        
    })