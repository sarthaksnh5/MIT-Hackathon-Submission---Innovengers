from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import transaction
from .models import OCRImage, OCRResult, ContactExtraction
from .serializers import OCRImageSerializer, OCRResultSerializer, ContactExtractionSerializer
from contacts.models import Contact, ContactSource
from contacts.serializers import ContactSerializer
from .services import OCRService

class OCRImageViewSet(viewsets.ModelViewSet):
    """API endpoint for managing OCR images"""
    serializer_class = OCRImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['image_type', 'upload_date']
    
    def get_queryset(self):
        """Return OCR images for the current user"""
        return OCRImage.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user when creating an OCR image"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Process an image with OCR"""
        image = self.get_object()
        
        try:
            # Process the image with OCR
            ocr_data = OCRService.process_image(image.image.path)
            
            # Create or update OCR result
            ocr_result, created = OCRResult.objects.update_or_create(
                image=image,
                defaults={
                    'raw_text': ocr_data['raw_text'],
                    'processed_text': ocr_data['processed_text'],
                    'confidence': ocr_data['confidence']
                }
            )
            
            # Return the OCR result
            serializer = OCRResultSerializer(ocr_result)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def extract_contacts(self, request, pk=None):
        """Extract contact information from an OCR result"""
        image = self.get_object()
        
        # Make sure the image has an OCR result
        try:
            ocr_result = OCRResult.objects.get(image=image)
        except OCRResult.DoesNotExist:
            return Response(
                {'error': 'Process the image with OCR first'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract contact info from the OCR text
        contact_info = OCRService.extract_contact_info(ocr_result.processed_text)
        
        # If the request has manual_data, use that instead
        if 'manual_data' in request.data:
            manual_data = request.data['manual_data']
            for field in contact_info:
                if field in manual_data and manual_data[field]:
                    contact_info[field] = manual_data[field]
        
        # Create the contact with the extracted info
        with transaction.atomic():
            contact = Contact.objects.create(
                user=self.request.user,
                **contact_info
            )
            
            # Create a source for the contact
            ContactSource.objects.create(
                contact=contact,
                source_type='BUSINESS_CARD' if image.image_type == 'BUSINESS_CARD' else 'OTHER',
                date=timezone.now().date(),
                location=image.location,
                notes=f"Created from OCR image {image.original_filename}"
            )
            
            # Create the extraction record
            extraction = ContactExtraction.objects.create(
                ocr_result=ocr_result,
                contact=contact
            )
        
        # Return the contact info
        contact_serializer = ContactSerializer(contact)
        return Response(contact_serializer.data)

class OCRResultViewSet(viewsets.ModelViewSet):
    """API endpoint for managing OCR results"""
    serializer_class = OCRResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_verified', 'processed_date']
    
    def get_queryset(self):
        """Return OCR results for the current user's images"""
        return OCRResult.objects.filter(image__user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Mark an OCR result as verified"""
        ocr_result = self.get_object()
        
        # Update the OCR result
        ocr_result.is_verified = True
        ocr_result.verified_date = timezone.now()
        
        # If the request has updated_text, update the processed_text
        if 'updated_text' in request.data:
            ocr_result.processed_text = request.data['updated_text']
        
        ocr_result.save()
        
        # Return the updated OCR result
        serializer = self.get_serializer(ocr_result)
        return Response(serializer.data)

class ContactExtractionViewSet(viewsets.ModelViewSet):
    """API endpoint for managing contact extractions"""
    serializer_class = ContactExtractionSerializer
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        """Return contact extractions for the current user's OCR results"""
        return ContactExtraction.objects.filter(ocr_result__image__user=self.request.user)