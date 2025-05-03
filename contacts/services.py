from django.utils import timezone
import openai
from django.conf import settings

class MessageGeneratorService:
    """Service for generating connection messages"""
    
    @staticmethod
    def generate_connection_message(contact, linkedin_data=None, context=None):
        """Generate a personalized connection message"""
        # If using an LLM API like OpenAI, you would implement here
        try:
            # Set up context for message generation
            prompt_parts = [
                f"Write a personalized LinkedIn connection message to {contact.full_name} who works as {contact.job_title} at {contact.company}.",
                "The message should be friendly, professional, and under 200 characters.",
            ]
            
            # Add context if available
            if context:
                prompt_parts.append(f"Context for the connection: {context}")
                
            # Add LinkedIn data if available
            if linkedin_data:
                if linkedin_data.get('work_experiences'):
                    exp = linkedin_data['work_experiences'][0]
                    prompt_parts.append(f"They currently work as {exp.get('title')} at {exp.get('company_name')}.")
                
                if linkedin_data.get('posts'):
                    post = linkedin_data['posts'][0]
                    prompt_parts.append(f"They recently posted about: {post.get('content')[:100]}...")
                    
                if linkedin_data.get('mutual_connections'):
                    mutual = linkedin_data['mutual_connections'][0]
                    prompt_parts.append(f"You have a mutual connection: {mutual.get('name')}.")
            
            # You would call OpenAI API here in production
            # response = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     messages=[{"role": "system", "content": "\n".join(prompt_parts)}],
            #     max_tokens=100
            # )
            # message = response.choices[0].message.content.strip()
            
            # For demo purposes just create a simple message
            message = f"Hi {contact.first_name}, I enjoyed meeting you! I'd love to connect and explore potential collaborations between {contact.company} and my organization."
            
            # Ensure the message is under 200 characters
            if len(message) > 200:
                message = message[:197] + "..."
                
            return message
            
        except Exception as e:
            # In case of any error, fall back to a generic message
            return f"Hi {contact.first_name}, it was great connecting with you. I'd like to add you to my professional network."