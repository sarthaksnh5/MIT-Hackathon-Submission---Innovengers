from rest_framework import serializers
from .models import (
    LinkedInProfile, WorkExperience, VolunteeringExperience,
    Post, MutualConnection
)

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = [
            'id', 'company_name', 'title', 'location', 'description',
            'start_date', 'end_date', 'is_current'
        ]

class VolunteeringExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteeringExperience
        fields = [
            'id', 'organization_name', 'role', 'description',
            'start_date', 'end_date', 'is_current'
        ]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'content', 'post_url', 'post_date',
            'likes_count', 'comments_count'
        ]

class MutualConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutualConnection
        fields = ['id', 'name', 'profile_url', 'username', 'headline']

class LinkedInProfileSerializer(serializers.ModelSerializer):
    work_experiences = WorkExperienceSerializer(many=True, read_only=True)
    volunteering_experiences = VolunteeringExperienceSerializer(many=True, read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    mutual_connections = MutualConnectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = LinkedInProfile
        fields = [
            'id', 'contact', 'username', 'profile_url', 'headline',
            'location', 'industry', 'connections_count', 'followers_count',
            'about', 'last_updated', 'work_experiences', 'volunteering_experiences',
            'posts', 'mutual_connections'
        ]
        read_only_fields = ['last_updated']