from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from contacts.views import (
    ContactViewSet, ContactSourceViewSet, 
    ContactInteractionViewSet, ConnectionMessageViewSet
)
from ocr.views import (
    OCRImageViewSet, OCRResultViewSet, 
    ContactExtractionViewSet
)
from linkedin.views import (
    LinkedInProfileViewSet, WorkExperienceViewSet,
    VolunteeringExperienceViewSet, PostViewSet, 
    MutualConnectionViewSet
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import RegisterView

# Add to existing imports
from chat.views import ChatMessageViewSet, ContactQueryViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Personal CRM API",
        default_version='v1',
        description="API documentation for Personal CRM application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@personalcrm.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Create a router and register our viewsets
router = DefaultRouter()

# Contacts app
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'contact-sources', ContactSourceViewSet, basename='contactsource')
router.register(r'contact-interactions', ContactInteractionViewSet, basename='contactinteraction')
router.register(r'connection-messages', ConnectionMessageViewSet, basename='connectionmessage')

# OCR app
router.register(r'ocr-images', OCRImageViewSet, basename='ocrimage')
router.register(r'ocr-results', OCRResultViewSet, basename='ocrresult')
router.register(r'contact-extractions', ContactExtractionViewSet, basename='contactextraction')

# LinkedIn app
router.register(r'linkedin-profiles', LinkedInProfileViewSet, basename='linkedinprofile')
router.register(r'work-experiences', WorkExperienceViewSet, basename='workexperience')
router.register(r'volunteer-experiences', VolunteeringExperienceViewSet, basename='volunteeringexperience')
router.register(r'linkedin-posts', PostViewSet, basename='post')
router.register(r'mutual-connections', MutualConnectionViewSet, basename='mutualconnection')

router.register(r'chat-messages', ChatMessageViewSet, basename='chatmessage')
router.register(r'contact-queries', ContactQueryViewSet, basename='contactquery')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    # Swagger documentation paths
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Register
    path('api/auth/register/', RegisterView.as_view(), name='register'),

    # Login (Token Obtain)
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Token Refresh
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)