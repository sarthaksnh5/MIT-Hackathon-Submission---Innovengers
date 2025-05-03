from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contact, ContactSource, ContactInteraction, ConnectionMessage
from .serializers import (
    ContactSerializer, ContactSourceSerializer, 
    ContactInteractionSerializer, ConnectionMessageSerializer
)
from .services import MessageGeneratorService
from linkedin.services import LinkedInService

class ContactViewSet(viewsets.ModelViewSet):
    """API endpoint for managing contacts"""
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'job_title']
    search_fields = ['first_name', 'last_name', 'email', 'company', 'job_title']
    ordering_fields = ['first_name', 'last_name', 'created_at', 'updated_at']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        """Return contacts for the current user"""
        return Contact.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user when creating a contact"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate_message(self, request, pk=None):
        """Generate a connection message for the contact"""
        contact = self.get_object()
        context = request.data.get('context', '')
        
        # If the contact has LinkedIn data, fetch it
        linkedin_data = None
        if contact.linkedin_username:
            try:
                # In a real app, you'd want to cache this data or check if it exists already
                linkedin_data = LinkedInService.get_profile_data(contact.linkedin_username)
            except Exception as e:
                # Log the error but continue without LinkedIn data
                pass
        
        # Generate message
        message_text = MessageGeneratorService.generate_connection_message(
            contact, linkedin_data, context
        )
        
        # Save the message
        message = ConnectionMessage.objects.create(
            contact=contact,
            message_text=message_text
        )
        
        serializer = ConnectionMessageSerializer(message)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages for a contact"""
        contact = self.get_object()
        messages = contact.messages.all()
        serializer = ConnectionMessageSerializer(messages, many=True)
        return Response(serializer.data)

class ContactSourceViewSet(viewsets.ModelViewSet):
    """API endpoint for managing contact sources"""
    serializer_class = ContactSourceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['source_type', 'event_name', 'location']
    ordering_fields = ['date', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return contact sources for the current user's contacts"""
        return ContactSource.objects.filter(contact__user=self.request.user)

class ContactInteractionViewSet(viewsets.ModelViewSet):
    """API endpoint for managing contact interactions"""
    serializer_class = ContactInteractionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['interaction_type', 'date']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        """Return contact interactions for the current user's contacts"""
        return ContactInteraction.objects.filter(contact__user=self.request.user)

class ConnectionMessageViewSet(viewsets.ModelViewSet):
    """API endpoint for managing connection messages"""
    serializer_class = ConnectionMessageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_sent']
    ordering_fields = ['created_at', 'sent_date']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return connection messages for the current user's contacts"""
        return ConnectionMessage.objects.filter(contact__user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_sent(self, request, pk=None):
        """Mark a message as sent"""
        message = self.get_object()
        message.is_sent = True
        message.sent_date = timezone.now()
        message.save()
        serializer = self.get_serializer(message)
        return Response(serializer.data)