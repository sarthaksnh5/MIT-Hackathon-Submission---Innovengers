from django.contrib import admin
from .models import Contact, ContactSource, ContactInteraction, ConnectionMessage

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'company', 'job_title', 'created_at']
    list_filter = ['company', 'created_at', 'updated_at']
    search_fields = ['first_name', 'last_name', 'email', 'company', 'job_title']
    date_hierarchy = 'created_at'

@admin.register(ContactSource)
class ContactSourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'contact', 'source_type', 'event_name', 'date', 'created_at']
    list_filter = ['source_type', 'date', 'created_at']
    search_fields = ['contact__first_name', 'contact__last_name', 'event_name']
    date_hierarchy = 'created_at'

@admin.register(ContactInteraction)
class ContactInteractionAdmin(admin.ModelAdmin):
    list_display = ['id', 'contact', 'interaction_type', 'date', 'created_at']
    list_filter = ['interaction_type', 'date', 'created_at']
    search_fields = ['contact__first_name', 'contact__last_name', 'notes']
    date_hierarchy = 'date'

@admin.register(ConnectionMessage)
class ConnectionMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'contact', 'is_sent', 'sent_date', 'created_at']
    list_filter = ['is_sent', 'sent_date', 'created_at']
    search_fields = ['contact__first_name', 'contact__last_name', 'message_text']
    date_hierarchy = 'created_at'