import json
import pytesseract
from django.conf import settings
from PIL import Image
import openai

class OCRService:
    """Service for handling OCR operations"""

    def process_text(text):
        prompt = """Here is the raw data extracted from image using OCR. If possible extract the contact information from it.
        Contract information should be:
        first_name, last_name, email, phone_number, company, job_title

        return it into JSON format.

        If you are not sure about the information, please return empty string.
        Here is the data:
        {text}
        """
        # Call OpenAI API with the prompt (openai>=1.0.0)
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt.format(text=text)}
            ],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        # Extract the response text
        response_text = response.choices[0].message.content
        return response_text
    
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
            ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence
            confidences = [int(conf) for conf in ocr_data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Get full text
            raw_text = pytesseract.image_to_string(img)
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
                'confidence': avg_confidence / 100.0,
            }
        except Exception as e:
            raise Exception(f"OCR processing error: {str(e)}")