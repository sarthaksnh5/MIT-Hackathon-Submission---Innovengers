from django.db import models
from contacts.models import Contact

class LinkedInProfile(models.Model):
    """Model for storing LinkedIn profile information"""
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='linkedin_profile')
    username = models.CharField(max_length=255)
    profile_url = models.URLField(max_length=500)
    headline = models.CharField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    connections_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    about = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"LinkedIn: {self.contact.full_name} ({self.username})"

class WorkExperience(models.Model):
    """Model for storing LinkedIn work experiences"""
    linkedin_profile = models.ForeignKey(LinkedInProfile, on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_current', '-start_date']
    
    def __str__(self):
        return f"{self.title} at {self.company_name}"

class VolunteeringExperience(models.Model):
    """Model for storing LinkedIn volunteering experiences"""
    linkedin_profile = models.ForeignKey(LinkedInProfile, on_delete=models.CASCADE, related_name='volunteering_experiences')
    organization_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_current', '-start_date']
    
    def __str__(self):
        return f"{self.role} at {self.organization_name}"

class Post(models.Model):
    """Model for storing LinkedIn posts"""
    linkedin_profile = models.ForeignKey(LinkedInProfile, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    post_url = models.URLField(max_length=500, blank=True, null=True)
    post_date = models.DateTimeField()
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-post_date']
    
    def __str__(self):
        return f"Post by {self.linkedin_profile.contact.full_name} on {self.post_date.strftime('%Y-%m-%d')}"

class MutualConnection(models.Model):
    """Model for storing mutual connections on LinkedIn"""
    linkedin_profile = models.ForeignKey(LinkedInProfile, on_delete=models.CASCADE, related_name='mutual_connections')
    name = models.CharField(max_length=255)
    profile_url = models.URLField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    headline = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - Mutual with {self.linkedin_profile.contact.full_name}"