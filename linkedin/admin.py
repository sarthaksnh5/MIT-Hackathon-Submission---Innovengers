from django.contrib import admin
from .models import (
    LinkedInProfile, WorkExperience, VolunteeringExperience,
    Post, MutualConnection
)

@admin.register(LinkedInProfile)
class LinkedInProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'contact', 'username', 'headline', 'connections_count', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['contact__first_name', 'contact__last_name', 'username', 'headline']
    date_hierarchy = 'last_updated'

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['id', 'linkedin_profile', 'company_name', 'title', 'is_current']
    list_filter = ['is_current', 'start_date', 'end_date']
    search_fields = ['linkedin_profile__contact__first_name', 'linkedin_profile__contact__last_name', 
                     'company_name', 'title']

@admin.register(VolunteeringExperience)
class VolunteeringExperienceAdmin(admin.ModelAdmin):
    list_display = ['id', 'linkedin_profile', 'organization_name', 'role', 'is_current']
    list_filter = ['is_current', 'start_date', 'end_date']
    search_fields = ['linkedin_profile__contact__first_name', 'linkedin_profile__contact__last_name',
                     'organization_name', 'role']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'linkedin_profile', 'post_date', 'likes_count', 'comments_count']
    list_filter = ['post_date']
    search_fields = ['linkedin_profile__contact__first_name', 'linkedin_profile__contact__last_name',
                     'content']
    date_hierarchy = 'post_date'

@admin.register(MutualConnection)
class MutualConnectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'linkedin_profile', 'name', 'headline']
    search_fields = ['linkedin_profile__contact__first_name', 'linkedin_profile__contact__last_name',
                     'name', 'headline']