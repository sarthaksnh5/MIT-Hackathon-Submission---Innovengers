from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    """Model for storing contact information"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    linkedin_url = models.URLField(max_length=500, blank=True, null=True)
    linkedin_username = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        unique_together = ('user', 'first_name', 'last_name')
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class ContactSource(models.Model):
    """Model for storing where/how the contact was acquired"""
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='sources')
    source_type = models.CharField(
        max_length=20,
        choices=[
            ('BUSINESS_CARD', 'Business Card'),
            ('CONFERENCE', 'Conference'),
            ('MEETING', 'Meeting'),
            ('SOCIAL_MEDIA', 'Social Media'),
            ('REFERRAL', 'Referral'),
            ('OTHER', 'Other'),
        ]
    )
    event_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_source_type_display()} - {self.contact}"

class ContactInteraction(models.Model):
    """Model for tracking interactions with contacts"""
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(
        max_length=20,
        choices=[
            ('EMAIL', 'Email'),
            ('CALL', 'Phone Call'),
            ('MEETING', 'Meeting'),
            ('MESSAGE', 'Message'),
            ('OTHER', 'Other'),
        ]
    )
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.get_interaction_type_display()} with {self.contact}"

class ConnectionMessage(models.Model):
    """Model for storing drafted connection messages"""
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='messages')
    message_text = models.TextField(max_length=200)  # LinkedIn limit is 200 chars
    is_sent = models.BooleanField(default=False)
    sent_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Message for {self.contact} ({'Sent' if self.is_sent else 'Draft'})"