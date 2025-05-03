from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact

class OCRImage(models.Model):
    """Model for storing images for OCR processing"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ocr_images')
    image = models.ImageField(upload_to='ocr_images/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    taken_date = models.DateTimeField(blank=True, null=True)
    image_type = models.CharField(
        max_length=20,
        choices=[
            ('BUSINESS_CARD', 'Business Card'),
            ('CONFERENCE_AGENDA', 'Conference Agenda'),
            ('OTHER', 'Other'),
        ],
        default='BUSINESS_CARD'
    )
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.original_filename} - {self.get_image_type_display()}"

class OCRResult(models.Model):
    """Model for storing OCR processing results"""
    image = models.OneToOneField(OCRImage, on_delete=models.CASCADE, related_name='ocr_result')
    raw_text = models.TextField()
    processed_text = models.TextField(blank=True, null=True)
    confidence = models.FloatField(default=0.0)
    processed_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"OCR Result for {self.image}"

class ContactExtraction(models.Model):
    """Model to link OCR results to extracted contacts"""
    ocr_result = models.ForeignKey(OCRResult, on_delete=models.CASCADE, related_name='extractions')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='extractions')
    extraction_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Extraction: {self.contact} from {self.ocr_result.image}"