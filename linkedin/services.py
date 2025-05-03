import requests
import json
from django.conf import settings
from .models import LinkedInProfile, WorkExperience, VolunteeringExperience, Post, MutualConnection

#!/usr/bin/env python3
"""
LinkedIn Profile Finder with LLM-based processing

This script uses Deepseek's API to process OCR text from business cards to extract
structured information, then searches for matching LinkedIn profiles.
"""

import re
import json
import requests
import argparse
from typing import Dict, List, Any, Optional, Tuple

# Import test data
from test_data import (
    TEST_CASE_0, TEST_CASE_1, TEST_CASE_2, TEST_CASE_3, TEST_CASE_4,
    TEST_CASE_5, TEST_CASE_6, TEST_CASE_7, TEST_CASE_8, TEST_CASE_9,
    TEST_CASE_10, TEST_CASE_11
)

# Import the LLM-based business card processor
from llm_card_processor import LLMBusinessCardProcessor


class LinkedInProfileFinder:
    """Search for LinkedIn profiles based on extracted business card information."""
    
    # API key for LinkedIn API
    API_KEY = "59a13c14f1msh0e4e4b6d650c622p1a375cjsn3f57cdeec48b"
    API_HOST = "linkedin-api8.p.rapidapi.com"
    
    def __init__(self):
        """Initialize with API credentials."""
        self.headers = {
            "X-RapidAPI-Key": self.API_KEY,
            "X-RapidAPI-Host": self.API_HOST
        }
    
    def construct_search_params(self, card_info: Dict[str, Any]) -> Dict[str, str]:
        """
        Construct LinkedIn search parameters based on business card information.
        
        Args:
            card_info: Dictionary containing extracted business card information
            
        Returns:
            Dictionary of search parameters for LinkedIn API
        """
        # Initialize search parameters
        search_params = {}
        
        # Add name-related parameters
        if card_info['full_name']:
            # Use the full name as the primary keywords parameter
            search_params['keywords'] = card_info['full_name']
            
            # Also add first and last name as separate parameters if available
            if card_info['first_name']:
                search_params['firstName'] = card_info['first_name']
            if card_info['last_name']:
                search_params['lastName'] = card_info['last_name']
        
        # Add company as a parameter if available
        if card_info['company']:
            search_params['company'] = card_info['company']
        
        # Add job title as a keyword title if available
        if card_info['job_title']:
            search_params['keywordTitle'] = card_info['job_title']
        
        # Default starting position for results
        search_params['start'] = '0'
        
        # Default maximum number of results
        search_params['max'] = '10'
        
        return search_params
    
    def search_profiles(self, search_params: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Search for LinkedIn profiles using the provided search parameters.
        
        Args:
            search_params: Dictionary of search parameters for LinkedIn API
            
        Returns:
            List of matching LinkedIn profiles
        """
        # Construct the URL for the LinkedIn API search endpoint
        url = f"https://{self.API_HOST}/search-people"
        
        # Debug: Print detailed request information
        print("\n=== API REQUEST DETAILS ===")
        print(f"URL: {url}")
        print("Headers:")
        # Print headers but mask the API key for security
        safe_headers = self.headers.copy()
        if 'X-RapidAPI-Key' in safe_headers:
            key = safe_headers['X-RapidAPI-Key']
            masked_key = key[:8] + '*' * (len(key) - 12) + key[-4:]
            safe_headers['X-RapidAPI-Key'] = masked_key
        print(json.dumps(safe_headers, indent=2))
        
        print("Parameters:")
        print(json.dumps(search_params, indent=2))
        
        try:
            # Make the API request
            response = requests.get(url, headers=self.headers, params=search_params)
            response.raise_for_status()
            
            # Parse the JSON response
            data = response.json()
            
            # Debug: Print detailed response information
            print("\n=== API RESPONSE DETAILS ===")
            print(f"Status Code: {response.status_code}")
            print("Response Headers:")
            print(json.dumps(dict(response.headers), indent=2))
            print("Full JSON Response:")
            print(json.dumps(data, indent=2))
            
            # Extract relevant profile information from the response
            profiles = []
            
            # Check if the response is successful and has the expected structure
            if (isinstance(data, dict) and data.get('success') and 
                'data' in data and isinstance(data['data'], dict) and 
                'items' in data['data'] and isinstance(data['data']['items'], list)):
                
                # Process each profile in the items list
                for profile_data in data['data']['items']:
                    if isinstance(profile_data, dict):
                        # Extract basic profile information
                        profile_info = {
                            'name': profile_data.get('fullName', ''),
                            'headline': profile_data.get('headline', ''),
                            'location': profile_data.get('location', '') if isinstance(profile_data.get('location'), str) else 
                                      profile_data.get('location', {}).get('name', '') if isinstance(profile_data.get('location'), dict) else '',
                            'profile_id': profile_data.get('username', ''),
                            'profile_url': profile_data.get('profileURL', ''),  # Use the direct profileURL from the API
                            'industry': profile_data.get('industry', ''),
                            'company': '',
                            'position': '',
                            'image_url': profile_data.get('profilePicture', '') if isinstance(profile_data.get('profilePicture'), str) else 
                                        profile_data.get('profilePicture', {}).get('displayImage', '') if isinstance(profile_data.get('profilePicture'), dict) else ''
                        }
                        
                        # Extract current position and company
                        if 'currentPositions' in profile_data and isinstance(profile_data['currentPositions'], list) and profile_data['currentPositions']:
                            current_position = profile_data['currentPositions'][0]
                            if isinstance(current_position, dict):
                                profile_info['position'] = current_position.get('title', '')
                                profile_info['company'] = current_position.get('companyName', '')
                        
                        # Add experience information if available
                        if 'pastPositions' in profile_data and isinstance(profile_data['pastPositions'], list):
                            profile_info['experience'] = []
                            for exp in profile_data['pastPositions'][:3]:  # Limit to first 3 experiences
                                if isinstance(exp, dict):
                                    exp_info = {
                                        'title': exp.get('title', ''),
                                        'company': exp.get('companyName', ''),
                                        'duration': f"{exp.get('startDate', '')} - {exp.get('endDate', '')}"
                                    }
                                    profile_info['experience'].append(exp_info)
                        
                        # Add education information if available
                        if 'education' in profile_data and isinstance(profile_data['education'], list):
                            profile_info['education'] = []
                            for edu in profile_data['education'][:2]:  # Limit to first 2 education entries
                                if isinstance(edu, dict):
                                    edu_info = {
                                        'school': edu.get('schoolName', ''),
                                        'degree': edu.get('degree', ''),
                                        'field': edu.get('fieldOfStudy', '')
                                    }
                                    profile_info['education'].append(edu_info)
                        
                        profiles.append(profile_info)
                
                print(f"\nFound {len(profiles)} profiles in the API response.")
                
            # If the response doesn't have the expected structure but is still successful
            elif isinstance(data, dict) and data.get('success'):
                print("\nAPI request was successful, but no profiles were found or the response format is unexpected.")
                
                # If there's a message in the response, print it
                if 'message' in data:
                    print(f"API Message: {data['message']}")
                
                # Print the full response for debugging (truncated if too long)
                full_response = json.dumps(data, indent=2)
                print(f"\nFull API Response (truncated):\n{full_response[:500]}..." if len(full_response) > 500 else full_response)
                
            # If the response indicates an error
            else:
                print("\nAPI request was not successful or returned an unexpected format.")
                
                # If there's an error message, print it
                if isinstance(data, dict) and 'message' in data:
                    print(f"API Error Message: {data['message']}")
                
                # Create a mock profile with the error information
                profiles.append({
                    'name': 'API Error',
                    'headline': 'The API request did not return the expected data',
                    'raw_response': str(data)[:200] + '...' if len(str(data)) > 200 else str(data)
                })
            
            return profiles
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching LinkedIn profiles: {e}")
            return []
    
    def search_by_name(self, name: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for LinkedIn profiles by name.
        
        Args:
            name: Person's name to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of matching LinkedIn profiles
        """
        search_params = {
            'keywords': name,
            'max': str(max_results),
            'start': '0'
        }
        
        return self.search_profiles(search_params)
    
    def search_by_name_and_company(self, name: str, company: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for LinkedIn profiles by name and company.
        
        Args:
            name: Person's name to search for
            company: Company name to filter by
            max_results: Maximum number of results to return
            
        Returns:
            List of matching LinkedIn profiles
        """
        search_params = {
            'keywords': name,
            'company': company,
            'max': str(max_results),
            'start': '0'
        }
        
        return self.search_profiles(search_params)


def process_business_card(ocr_text: List[str]) -> None:
    """
    Process a business card OCR text array using LLM and search for matching LinkedIn profiles.
    
    Implements a tiered search strategy:
    1. Try full name + company in keywords
    2. If no results, try full name + job title in keywords
    3. If still no results, try just full name in keywords
    
    Args:
        ocr_text: List of strings from OCR processing
    """
    print("Processing business card OCR text...")
    
    # Process the business card using the LLM processor
    processor = LLMBusinessCardProcessor(ocr_text)
    card_info = processor.extract_information()
    
    print("\nExtracted Information from LLM:")
    print(json.dumps(card_info, indent=2))
    
    # Initialize the LinkedIn profile finder
    finder = LinkedInProfileFinder()
    
    # Check if we have the required fields for search
    has_name = bool(card_info['full_name'])
    has_company = bool(card_info['company'])
    has_job_title = bool(card_info['job_title'])
    
    if not has_name:
        print("\nERROR: No name found in the business card. Cannot perform LinkedIn search.")
        return
    
    # TIER 1: Search with full name + company in keywords
    if has_name and has_company:
        print("\n=== TIER 1 SEARCH: Full Name + Company ===")
        search_params = {
            'keywords': f"{card_info['full_name']} {card_info['company']}",
            'start': '0',
            'max': '10'
        }
        
        print(f"Searching with parameters:")
        print(json.dumps(search_params, indent=2))
        
        profiles = finder.search_profiles(search_params)
        
        # If we found results, return them
        if profiles:
            print("\nFound results with TIER 1 search (name + company).")
            display_profiles(profiles)
            return
    
    # TIER 2: Search with full name + job title in keywords
    if has_name and has_job_title:
        print("\n=== TIER 2 SEARCH: Full Name + Job Title ===")
        search_params = {
            'keywords': f"{card_info['full_name']} {card_info['job_title']}",
            'start': '0',
            'max': '10'
        }
        
        print(f"Searching with parameters:")
        print(json.dumps(search_params, indent=2))
        
        profiles = finder.search_profiles(search_params)
        
        # If we found results, return them
        if profiles:
            print("\nFound results with TIER 2 search (name + job title).")
            display_profiles(profiles)
            return
    
    # TIER 3: Search with just full name
    print("\n=== TIER 3 SEARCH: Full Name Only ===")
    search_params = {
        'keywords': card_info['full_name'],
        'start': '0',
        'max': '10'
    }
    
    print(f"Searching with parameters:")
    print(json.dumps(search_params, indent=2))
    
    profiles = finder.search_profiles(search_params)
    
    if profiles:
        print("\nFound results with TIER 3 search (name only).")
        display_profiles(profiles)
    else:
        print("\nNo matching LinkedIn profiles found after all search attempts.")


def display_profiles(profiles: List[Dict[str, Any]]) -> None:
    """
    Display the LinkedIn profiles in a formatted way.
    
    Args:
        profiles: List of LinkedIn profile dictionaries
    """
    print("\nMatching LinkedIn Profiles:")
    for i, profile in enumerate(profiles, 1):
        print(f"\nProfile {i}:")
        print(f"Name: {profile['name']}")
        print(f"Headline: {profile['headline']}")
        
        if 'location' in profile and profile['location']:
            print(f"Location: {profile['location']}")
        
        if 'position' in profile and profile['position']:
            print(f"Current Position: {profile['position']}")
        
        if 'company' in profile and profile['company']:
            print(f"Current Company: {profile['company']}")
        
        if 'profile_url' in profile and profile['profile_url']:
            print(f"Profile URL: {profile['profile_url']}")
        
        # Display experience if available
        if 'experience' in profile and profile['experience']:
            print("\nExperience:")
            for exp in profile['experience']:
                print(f"  - {exp['title']} at {exp['company']} ({exp['duration']})")
        
        # Display education if available
        if 'education' in profile and profile['education']:
            print("\nEducation:")
            for edu in profile['education']:
                print(f"  - {edu['degree']} in {edu['field']} at {edu['school']}")
        
        # Display raw response if available (for debugging)
        if 'raw_response' in profile:
            print(f"\nAPI Response: {profile['raw_response']}")

class LinkedInService:
    """Service for handling LinkedIn API operations"""
    
    @staticmethod
    def get_profile_data(username):
        """Fetch LinkedIn profile data using the RapidAPI endpoint"""
        # url = "https://linkedin-api8.p.rapidapi.com/"
        
        # querystring = {"username": username}
        
        # headers = {
        #     "X-RapidAPI-Key": settings.LINKEDIN_RAPIDAPI_KEY,
        #     "X-RapidAPI-Host": settings.LINKEDIN_RAPIDAPI_HOST
        # }
        
        # try:
        #     response = requests.get(url, headers=headers, params=querystring)
        #     response.raise_for_status()  # Raise exception for 4XX/5XX responses
        #     return response.json()
        # except requests.exceptions.RequestException as e:
        #     raise Exception(f"LinkedIn API error: {str(e)}")
        finder = LinkedInProfileFinder()
        finder.search_profiles()
    
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