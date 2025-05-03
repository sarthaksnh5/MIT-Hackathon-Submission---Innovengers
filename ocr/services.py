import json
import pytesseract
from django.conf import settings
from PIL import Image
import openai
import re

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

class OCRService:
    """Service for handling OCR operations"""

    def process_text(text):
        # prompt = """Here is the raw data extracted from image using OCR. If possible extract the contact information from it.
        # Contract information should be:
        # first_name, last_name, email, phone_number, company, job_title

        # return it into JSON format.

        # If you are not sure about the information, please return empty string.
        # Here is the data:
        # {text}
        # """
        # # Call OpenAI API with the prompt (openai>=1.0.0)
        # client = openai.OpenAI()
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "user", "content": prompt.format(text=text)}
        #     ],
        #     max_tokens=1000,
        #     n=1,
        #     stop=None,
        #     temperature=0.5,
        # )
        # # Extract the response text
        # response_text = response.choices[0].message.content
        # return response_text        
        data = LLMBusinessCardProcessor(ocr_text=text).extract_information()
        data = json.dumps(data)
        return data
    
    @staticmethod
    def process_image(image_path):
        """Process an image using OCR and return the extracted text"""
        # Configure pytesseract path if set in settings
        if hasattr(settings, 'TESSERACT_CMD'):
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD                

        try:
            # Open the image
            img = Image.open(image_path)
            
            # Process image with OCR
            custom_config = r'--oem 1 --psm 11'
            arr = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_config)
            
            # Calculate average confidence
            # confidences = [int(conf) for conf in ocr_data['conf'] if conf != '-1']
            # print("Processing text with OpenAI API...")
            # avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Get full text
            raw_text = pytesseract.image_to_string(img)
            # raw_text = re.findall('(?<=\t(?:8[6-9]|9\d)\t)[a-zA-Z]+(?=,?\.?\n)', arr)
            processed_text = {}

            try:
                # Process the raw text with OpenAI API
                processed_text = OCRService.process_text(raw_text)
                processed_text = json.loads(processed_text)
                processed_text = json.dumps(processed_text)
            except json.JSONDecodeError:
                # Handle JSON decoding error
                processed_text = {}
                print(f"Error decoding JSON: {processed_text}")
            except Exception as e:
                pass
            
            return {
                'raw_text': raw_text,
                'processed_text': processed_text,  # Can be further processed if necessary
                'confidence': 0,
            }
        except Exception as e:
            raise Exception(f"OCR processing error: {str(e)}")