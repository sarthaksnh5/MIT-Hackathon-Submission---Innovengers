from rest_framework import serializers
from .models import OCRImage, OCRResult, ContactExtraction
from contacts.serializers import ContactSerializer

class OCRImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRImage
        fields = [
            'id', 'image', 'original_filename', 'upload_date', 
            'location', 'taken_date', 'image_type'
        ]
        read_only_fields = ['upload_date', 'original_filename']

    def create(self, validated_data):
        validated_data['original_filename'] = validated_data['image'].name
        return super().create(validated_data)

class OCRResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRResult
        fields = [
            'id', 'image', 'raw_text', 'processed_text', 
            'confidence', 'processed_date', 'is_verified', 'verified_date'
        ]
        read_only_fields = ['processed_date']

class ContactExtractionSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    
    class Meta:
        model = ContactExtraction
        fields = ['id', 'ocr_result', 'contact', 'extraction_date']
        read_only_fields = ['extraction_date']