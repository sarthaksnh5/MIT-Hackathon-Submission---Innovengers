from django.contrib import admin
from .models import ChatMessage, ContactQuery

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_from_user', 'message_preview', 'created_at']
    list_filter = ['is_from_user', 'created_at']
    search_fields = ['message', 'user__username']
    date_hierarchy = 'created_at'
    
    def message_preview(self, obj):
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    message_preview.short_description = 'Message'

@admin.register(ContactQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ['id', 'contact', 'query_type', 'resolved']
    list_filter = ['query_type', 'resolved']
    search_fields = ['contact__first_name', 'contact__last_name', 'chat_message__message']