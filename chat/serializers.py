from rest_framework import serializers
from .models import ChatMessage, ContactQuery
from contacts.serializers import ContactSerializer

class ChatMessageSerializer(serializers.ModelSerializer):
    related_contact_details = ContactSerializer(source='related_contact', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'is_from_user', 'message', 'image', 'created_at',
            'related_contact', 'related_contact_details'
        ]
        read_only_fields = ['created_at']
        
class ContactQuerySerializer(serializers.ModelSerializer):
    chat_message_details = ChatMessageSerializer(source='chat_message', read_only=True)
    contact_details = ContactSerializer(source='contact', read_only=True)
    
    class Meta:
        model = ContactQuery
        fields = [
            'id', 'chat_message', 'contact', 'query_type', 
            'resolved', 'chat_message_details', 'contact_details'
        ]