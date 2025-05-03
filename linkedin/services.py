import requests
import json
from django.conf import settings
from .models import LinkedInProfile, WorkExperience, VolunteeringExperience, Post, MutualConnection

class LinkedInService:
    """Service for handling LinkedIn API operations"""
    
    @staticmethod
    def get_profile_data(username):
        """Fetch LinkedIn profile data using the RapidAPI endpoint"""
        url = "https://linkedin-api8.p.rapidapi.com/"
        
        querystring = {"username": username}
        
        headers = {
            "X-RapidAPI-Key": settings.LINKEDIN_RAPIDAPI_KEY,
            "X-RapidAPI-Host": settings.LINKEDIN_RAPIDAPI_HOST
        }
        
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"LinkedIn API error: {str(e)}")
    
    @staticmethod
    def save_profile_data(contact, profile_data):
        """Save LinkedIn profile data to database"""
        # Create or update the LinkedIn profile
        profile, created = LinkedInProfile.objects.update_or_create(
            contact=contact,
            defaults={
                'username': profile_data.get('username', ''),
                'profile_url': profile_data.get('public_id', ''),
                'headline': profile_data.get('headline', ''),
                'location': profile_data.get('location', {}).get('default', ''),
                'industry': profile_data.get('industry', ''),
                'connections_count': profile_data.get('connections', 0),
                'followers_count': profile_data.get('followers', 0),
                'about': profile_data.get('about', '')
            }
        )
        
        # Save work experiences
        if 'experiences' in profile_data:
            # Clear existing experiences to avoid duplicates
            WorkExperience.objects.filter(linkedin_profile=profile).delete()
            
            for exp in profile_data['experiences']:
                WorkExperience.objects.create(
                    linkedin_profile=profile,
                    company_name=exp.get('company_name', ''),
                    title=exp.get('title', ''),
                    location=exp.get('location', ''),
                    description=exp.get('description', ''),
                    start_date=exp.get('starts_at', {}).get('day', None),  # This will need proper date conversion
                    end_date=exp.get('ends_at', {}).get('day', None),  # This will need proper date conversion
                    is_current=exp.get('is_current', False)
                )
        
        # Save volunteering experiences
        if 'volunteer_experiences' in profile_data:
            # Clear existing volunteer experiences
            VolunteeringExperience.objects.filter(linkedin_profile=profile).delete()
            
            for vol in profile_data['volunteer_experiences']:
                VolunteeringExperience.objects.create(
                    linkedin_profile=profile,
                    organization_name=vol.get('company_name', ''),
                    role=vol.get('title', ''),
                    description=vol.get('description', ''),
                    start_date=vol.get('starts_at', {}).get('day', None),  # This will need proper date conversion
                    end_date=vol.get('ends_at', {}).get('day', None),  # This will need proper date conversion
                    is_current=vol.get('is_current', False)
                )
        
        # Save posts (last 5)
        if 'posts' in profile_data:
            # Clear existing posts
            Post.objects.filter(linkedin_profile=profile).delete()
            
            # Take only the last 5 posts
            recent_posts = profile_data['posts'][:5]
            
            for post in recent_posts:
                Post.objects.create(
                    linkedin_profile=profile,
                    content=post.get('content', ''),
                    post_url=post.get('url', ''),
                    post_date=post.get('published_at', None),  # This will need proper date conversion
                    likes_count=post.get('likes_count', 0),
                    comments_count=post.get('comments_count', 0)
                )
        
        # Save mutual connections
        if 'mutual_connections' in profile_data:
            # Clear existing mutual connections
            MutualConnection.objects.filter(linkedin_profile=profile).delete()
            
            for connection in profile_data['mutual_connections']:
                MutualConnection.objects.create(
                    linkedin_profile=profile,
                    name=connection.get('name', ''),
                    profile_url=connection.get('url', ''),
                    username=connection.get('username', ''),
                    headline=connection.get('headline', '')
                )
        
        return profile