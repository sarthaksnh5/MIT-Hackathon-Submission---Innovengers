from django.utils import timezone
from contacts.models import Contact
import re
from PIL import Image
import pytesseract
import os
from django.conf import settings
from ocr.services import OCRService

class ChatAIService:
    """Service for processing and responding to chat messages"""
    
    @staticmethod
    def process_message(message_text, user, image_path=None):
        """Process a message and generate a response"""
        # Check if message contains a question about a specific contact
        related_contact = ChatAIService._identify_related_contact(message_text, user)
        
        # If image was provided, try to identify the person
        if image_path:
            return ChatAIService._process_image_query(image_path, user, message_text)
        
        # Generate response based on message content
        if related_contact:
            return ChatAIService._generate_contact_response(message_text, related_contact)
        else:
            return ChatAIService._generate_general_response(message_text, user)
    
    @staticmethod
    def _identify_related_contact(message_text, user):
        """Try to identify which contact the message is about"""
        # Get all contacts for the user
        contacts = Contact.objects.filter(user=user)
        
        # Check if any contact's name is mentioned in the message
        for contact in contacts:
            full_name = f"{contact.first_name} {contact.last_name}".lower()
            if contact.first_name.lower() in message_text.lower() or \
               contact.last_name.lower() in message_text.lower() or \
               full_name in message_text.lower():
                return contact
        
        return None
    
    @staticmethod
    def _process_image_query(image_path, user, message_text):
        """Process an image query to identify a person"""
        # Use OCR to extract text from image if it's a business card
        try:
            ocr_data = OCRService.process_image(image_path)
            extracted_info = OCRService.extract_contact_info(ocr_data['raw_text'])
            
            # Try to match with existing contacts
            potential_matches = []
            
            if extracted_info['first_name'] or extracted_info['last_name']:
                # Search for contacts with matching names
                name_query = Contact.objects.filter(user=user)
                if extracted_info['first_name']:
                    name_query = name_query.filter(first_name__icontains=extracted_info['first_name'])
                if extracted_info['last_name']:
                    name_query = name_query.filter(last_name__icontains=extracted_info['last_name'])
                
                potential_matches = list(name_query)
            
            if potential_matches:
                contact = potential_matches[0]  # Take the first match
                return {
                    'message': f"I recognize this person as {contact.full_name}, who works at {contact.company} as {contact.job_title}. Is that correct?",
                    'related_contact': contact
                }
            else:
                # No match found
                return {
                    'message': "I couldn't identify this person in your contacts. Would you like to add them?",
                    'related_contact': None
                }
        except Exception as e:
            # If OCR fails or there's another error
            return {
                'message': f"I couldn't process this image properly. Please try again with a clearer image.",
                'related_contact': None
            }
    
    @staticmethod
    def _generate_contact_response(message_text, contact):
        """Generate a response about a specific contact"""
        # Extract the type of question (using simple keyword matching for demo)
        message_lower = message_text.lower()
        
        # Basic information request
        if re.search(r'who|what|tell me about', message_lower):
            return {
                'message': f"{contact.full_name} works at {contact.company} as {contact.job_title}. " +
                          (f"Their email is {contact.email}. " if contact.email else "") +
                          (f"Their phone number is {contact.phone_number}. " if contact.phone_number else "") +
                          (f"You can find them on LinkedIn at {contact.linkedin_url}" if contact.linkedin_url else ""),
                'related_contact': contact
            }
        
        # When did I meet them
        elif re.search(r'when|meet|met|first', message_lower):
            sources = contact.sources.all()
            if sources.exists():
                source = sources.first()
                return {
                    'message': f"You met {contact.first_name} at {source.event_name or 'an event'}" +
                              (f" on {source.date.strftime('%B %d, %Y')}" if source.date else "") +
                              (f" in {source.location}" if source.location else "") + ".",
                    'related_contact': contact
                }
            else:
                return {
                    'message': f"I don't have records of when you met {contact.first_name}.",
                    'related_contact': contact
                }
        
        # Recent interactions
        elif re.search(r'recent|latest|last|interact', message_lower):
            interactions = contact.interactions.all()
            if interactions.exists():
                interaction = interactions.first()
                return {
                    'message': f"Your most recent interaction with {contact.first_name} was a " +
                              f"{interaction.get_interaction_type_display().lower()} on " +
                              f"{interaction.date.strftime('%B %d, %Y')}.",
                    'related_contact': contact
                }
            else:
                return {
                    'message': f"I don't have records of any interactions with {contact.first_name}.",
                    'related_contact': contact
                }
        
        # LinkedIn info
        elif re.search(r'linkedin|work|job|company|experience', message_lower):
            try:
                linkedin_profile = contact.linkedin_profile
                experiences = linkedin_profile.work_experiences.all()
                if experiences.exists():
                    current = experiences.filter(is_current=True).first()
                    if current:
                        return {
                            'message': f"{contact.first_name} currently works as {current.title} at {current.company_name}. " +
                                      f"They have {experiences.count()} work experiences in their LinkedIn profile.",
                            'related_contact': contact
                        }
                    else:
                        exp = experiences.first()
                        return {
                            'message': f"{contact.first_name}'s most recent role was {exp.title} at {exp.company_name}.",
                            'related_contact': contact
                        }
                else:
                    return {
                        'message': f"I have {contact.first_name}'s LinkedIn profile, but no work experience data available.",
                        'related_contact': contact
                    }
            except:
                return {
                    'message': f"I don't have LinkedIn information for {contact.first_name}.",
                    'related_contact': contact
                }
        
        # Default response
        else:
            return {
                'message': f"That's {contact.full_name}. What specifically would you like to know about them?",
                'related_contact': contact
            }
    
    @staticmethod
    def _generate_general_response(message_text, user):
        """Generate a general response when no specific contact is mentioned"""
        message_lower = message_text.lower()
        
        # Count of contacts
        if re.search(r'how many contacts|contact count|number of contacts', message_lower):
            count = Contact.objects.filter(user=user).count()
            return {
                'message': f"You have {count} contacts in your CRM.",
                'related_contact': None
            }
        
        # Recent contacts
        elif re.search(r'recent contacts|newest contacts|last added', message_lower):
            recent_contacts = Contact.objects.filter(user=user).order_by('-created_at')[:3]
            if recent_contacts.exists():
                names = ", ".join([c.full_name for c in recent_contacts])
                return {
                    'message': f"Your most recently added contacts are: {names}.",
                    'related_contact': None
                }
            else:
                return {
                    'message': "You don't have any contacts yet.",
                    'related_contact': None
                }
        
        # Help
        elif re.search(r'help|what can you do|capabilities|functions', message_lower):
            return {
                'message': "I can help you manage your contacts. You can ask me about specific contacts, " +
                          "upload images to identify people, get summaries of your network, and more. " +
                          "Try asking 'Who is John Smith?' or 'Tell me about my recent contacts.'",
                'related_contact': None
            }
        
        # Default response
        else:
            return {
                'message': "I'm your Personal CRM assistant. How can I help you with your contacts today?",
                'related_contact': None
            }