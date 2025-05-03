from rest_framework import serializers
from .models import Contact, ContactSource, ContactInteraction, ConnectionMessage

class ContactSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSource
        fields = ['id', 'source_type', 'event_name', 'location', 'date', 'time', 'notes', 'created_at']

class ContactInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInteraction
        fields = ['id', 'interaction_type', 'date', 'notes', 'created_at']

class ConnectionMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionMessage
        fields = ['id', 'message_text', 'is_sent', 'sent_date', 'created_at']

class ContactSerializer(serializers.ModelSerializer):
    sources = ContactSourceSerializer(many=True, read_only=True)
    interactions = ContactInteractionSerializer(many=True, read_only=True)
    messages = ConnectionMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Contact
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 
            'phone_number', 'company', 'job_title', 'linkedin_url', 
            'linkedin_username', 'notes', 'created_at', 'updated_at',
            'sources', 'interactions', 'messages'
        ]
        read_only_fields = ['full_name', 'created_at', 'updated_at']