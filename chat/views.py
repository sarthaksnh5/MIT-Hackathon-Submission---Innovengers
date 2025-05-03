from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import ChatMessage, ContactQuery
from .serializers import ChatMessageSerializer, ContactQuerySerializer
from .services import ChatAIService

class ChatMessageViewSet(viewsets.ModelViewSet):
    """API endpoint for managing chat messages"""
    serializer_class = ChatMessageSerializer
    
    def get_queryset(self):
        """Return chat messages for the current user"""
        return ChatMessage.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Process the message and generate a response"""
        # Save the user's message
        user_message = serializer.save(user=self.request.user, is_from_user=True)
        
        # Process the image if provided
        image_path = None
        if user_message.image:
            image_path = user_message.image.path
        
        # Generate AI response
        try:
            response = ChatAIService.process_message(
                user_message.message, 
                self.request.user,
                image_path
            )
            
            # Create AI response message
            ai_message = ChatMessage.objects.create(
                user=self.request.user,
                is_from_user=False,
                message=response['message'],
                related_contact=response.get('related_contact')
            )
            
            # If the message is related to a specific contact and was a query
            if response.get('related_contact') and user_message.message.endswith('?'):
                ContactQuery.objects.create(
                    chat_message=user_message,
                    contact=response['related_contact'],
                    query_type='DETAILS'  # Default type, can be refined
                )
            
            # Return both the user message and AI response
            return Response({
                'user_message': ChatMessageSerializer(user_message).data,
                'ai_response': ChatMessageSerializer(ai_message).data
            })
            
        except Exception as e:
            # Handle errors gracefully
            ai_message = ChatMessage.objects.create(
                user=self.request.user,
                is_from_user=False,
                message=f"I'm sorry, I couldn't process that request properly. Error: {str(e)}"
            )
            return Response({
                'user_message': ChatMessageSerializer(user_message).data,
                'ai_response': ChatMessageSerializer(ai_message).data
            })

class ContactQueryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing contact queries"""
    serializer_class = ContactQuerySerializer
    
    def get_queryset(self):
        """Return contact queries for the current user"""
        return ContactQuery.objects.filter(chat_message__user=self.request.user)