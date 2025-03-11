from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from face_recognition.views import upload_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload_image, name='upload_image'),

    # Redirect root URL to /upload/
    path('', lambda request: redirect('upload_image', permanent=True)),
]

# Serve media files in development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
