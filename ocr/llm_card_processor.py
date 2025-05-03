#!/usr/bin/env python3
"""
LLM-based Business Card Processor using Deepseek API

This module replaces the rule-based BusinessCardProcessor with a more accurate
LLM-based approach that uses Deepseek's API to extract structured information.
"""

import json
import requests
from typing import Dict, List, Any, Optional


class LLMBusinessCardProcessor:
    """Process OCR text from business cards using Deepseek LLM API."""
    
    # Deepseek API key and endpoint
    API_KEY = "sk-3649a71dfe8345e8add31f8290e42988"
    API_URL = "https://api.deepseek.com/v1/chat/completions"
    
    def __init__(self, ocr_text: List[str]):
        """
        Initialize with OCR text array.
        
        Args:
            ocr_text: List of strings from OCR processing
        """
        self.ocr_text = ocr_text
        self.extracted_info = {
            'full_name': '',
            'first_name': '',
            'last_name': '',
            'job_title': '',
            'company': '',
            'email': '',
            'phone_numbers': [],
            'address': '',
            'website': '',
            'additional_info': []
        }
    
    def extract_information(self) -> Dict[str, Any]:
        """
        Process OCR text to extract structured information using Deepseek LLM.
        
        Returns:
            Dictionary containing extracted information
        """
        print("Extracting information using Deepseek LLM API...")
        
        # Format the OCR text for the prompt
        formatted_text = ' '.join(self.ocr_text)
        
        # Create the system message for the LLM
        system_message = """
        You are a professional business card parser. Your task is to extract structured information from OCR text of business cards. The order of the OCR output might have been shuffled and so you should exercise your judgement to parse the information together.
        Analyze the text carefully and extract the following information:
        - full_name: The person's full name
        - first_name: The person's first name
        - last_name: The person's last name
        - job_title: The person's job title or position
        - company: The company or organization name
        - email: The email address
        - phone_numbers: An array of phone numbers (include all numbers found)
        - address: The physical address
        - website: The website URL
        
        Return the information in a strict JSON format with these fields only.
        If a field cannot be identified, leave it as an empty string or empty array for phone_numbers.
        Make special effort to correctly identify the company name, as this is crucial.
        """
        
        # Create the user message with the OCR text
        user_message = f"Extract information from this business card OCR text:\n\n{formatted_text}"
        
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.API_KEY}"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.1,  # Low temperature for more deterministic output
            "response_format": {"type": "json_object"}  # Request JSON format
        }
        
        try:
            # Make the API request
            print("Sending request to Deepseek API...")
            response = requests.post(self.API_URL, headers=headers, json=data)
            response.raise_for_status()
            
            # Parse the JSON response
            result = response.json()
            
            # Debug info
            print(f"API Response Status: {response.status_code}")
            
            # Extract the generated content
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                
                # Parse the JSON content
                try:
                    parsed_content = json.loads(content)
                    print("Successfully parsed LLM response as JSON.")
                    
                    # Update the extracted_info with the parsed content
                    for key in self.extracted_info:
                        if key in parsed_content:
                            self.extracted_info[key] = parsed_content[key]
                    
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON from LLM response: {e}")
                    print(f"Raw content: {content}")
                    
                    # Fallback: Try to extract structured information from text response
                    self._extract_from_text_response(content)
            else:
                print("No choices in API response.")
                print(f"Full API response: {result}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
        
        return self.extracted_info
    
    def _extract_from_text_response(self, text: str) -> None:
        """
        Fallback method to extract information from text response if JSON parsing fails.
        
        Args:
            text: The text response from the LLM
        """
        print("Using fallback text extraction method...")
        
        # Look for patterns like "field_name: value" or "field_name = value"
        for line in text.split('\n'):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Try to split on common separators
            for separator in [':', '=', ' - ']:
                if separator in line:
                    key, value = line.split(separator, 1)
                    key = key.strip().lower().replace(' ', '_')
                    value = value.strip()
                    
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    
                    # Check if this key matches one of our expected fields
                    if key in self.extracted_info:
                        if key == 'phone_numbers':
                            # For phone numbers, append to the list
                            self.extracted_info[key].append(value)
                        else:
                            self.extracted_info[key] = value
                    
                    break  # Break after first successful separator match