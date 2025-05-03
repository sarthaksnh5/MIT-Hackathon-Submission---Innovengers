from django.contrib import admin
from .models import OCRImage, OCRResult, ContactExtraction

@admin.register(OCRImage)
class OCRImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'original_filename', 'image_type', 'upload_date']
    list_filter = ['image_type', 'upload_date']
    search_fields = ['user__username', 'original_filename', 'location']
    date_hierarchy = 'upload_date'

@admin.register(OCRResult)
class OCRResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'confidence', 'is_verified', 'processed_date', 'verified_date']
    list_filter = ['is_verified', 'processed_date', 'verified_date']
    search_fields = ['image__original_filename', 'raw_text', 'processed_text']
    date_hierarchy = 'processed_date'

@admin.register(ContactExtraction)
class ContactExtractionAdmin(admin.ModelAdmin):
    list_display = ['id', 'ocr_result', 'contact', 'extraction_date']
    list_filter = ['extraction_date']
    search_fields = ['contact__first_name', 'contact__last_name']
    date_hierarchy = 'extraction_date'