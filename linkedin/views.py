from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    LinkedInProfile, WorkExperience, VolunteeringExperience,
    Post, MutualConnection
)
from .serializers import (
    LinkedInProfileSerializer, WorkExperienceSerializer, 
    VolunteeringExperienceSerializer, PostSerializer, 
    MutualConnectionSerializer
)
from contacts.models import Contact
from .services import LinkedInService

class LinkedInProfileViewSet(viewsets.ModelViewSet):
    """API endpoint for managing LinkedIn profiles"""
    serializer_class = LinkedInProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact']
    
    def get_queryset(self):
        """Return LinkedIn profiles for the current user's contacts"""
        return LinkedInProfile.objects.filter(contact__user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def fetch_linkedin(self, request):
        try:
            # Fetch the profile data
            profile_data = LinkedInService.get_profile_data(request.data['username'])            
            
            return Response(profile_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def fetch_linkedin_data(self, request):
        """Fetch LinkedIn data for a contact"""
        if 'contact_id' not in request.data or 'username' not in request.data:
            return Response(
                {'error': 'Both contact_id and username are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the contact
        try:
            contact = Contact.objects.get(
                id=request.data['contact_id'],
                user=request.request.user
            )
        except Contact.DoesNotExist:
            return Response(
                {'error': 'Contact not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Fetch the LinkedIn data
        try:
            # Fetch the profile data
            profile_data = LinkedInService.get_profile_data(request.data['username'])
            
            # Save the profile data to the database
            profile = LinkedInService.save_profile_data(contact, profile_data)
            
            # Update the contact with the LinkedIn data
            contact.linkedin_username = request.data['username']
            contact.linkedin_url = profile.profile_url
            contact.save()
            
            # Return the profile data
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class WorkExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing work experiences"""
    serializer_class = WorkExperienceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['linkedin_profile', 'company_name', 'is_current']
    
    def get_queryset(self):
        """Return work experiences for the current user's contacts"""
        return WorkExperience.objects.filter(linkedin_profile__contact__user=self.request.user)

class VolunteeringExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing volunteering experiences"""
    serializer_class = VolunteeringExperienceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['linkedin_profile', 'organization_name', 'is_current']
    
    def get_queryset(self):
        """Return volunteering experiences for the current user's contacts"""
        return VolunteeringExperience.objects.filter(linkedin_profile__contact__user=self.request.user)

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing LinkedIn posts"""
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['linkedin_profile']
    
    def get_queryset(self):
        """Return posts for the current user's contacts"""
        return Post.objects.filter(linkedin_profile__contact__user=self.request.user)

class MutualConnectionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing mutual connections"""
    serializer_class = MutualConnectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['linkedin_profile']
    
    def get_queryset(self):
        """Return mutual connections for the current user's contacts"""
        return MutualConnection.objects.filter(linkedin_profile__contact__user=self.request.user)