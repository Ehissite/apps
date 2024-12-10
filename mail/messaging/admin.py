from django.contrib import admin
from .models import Conversation, ConversationMessages


# Register your models here.
admin.site.register(Conversation)
admin.site.register(ConversationMessages)
