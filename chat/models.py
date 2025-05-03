from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact

class ChatMessage(models.Model):
    """Model for storing chat messages"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    is_from_user = models.BooleanField(default=True)  # True if from user, False if from AI
    message = models.TextField()
    image = models.ImageField(upload_to='chat_images/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    related_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, 
                                        related_name='mentioned_in_chats', blank=True, null=True)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"{'User' if self.is_from_user else 'AI'} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class ContactQuery(models.Model):
    """Model for storing specific queries about contacts"""
    chat_message = models.OneToOneField(ChatMessage, on_delete=models.CASCADE, related_name='contact_query')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='queries')
    query_type = models.CharField(
        max_length=20,
        choices=[
            ('IDENTIFY', 'Identify Person'),
            ('DETAILS', 'Ask Details'),
            ('SUGGESTIONS', 'Get Suggestions'),
            ('OTHER', 'Other Query'),
        ]
    )
    resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Query about {self.contact.full_name} - {self.get_query_type_display()}"