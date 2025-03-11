from django.urls import path
from .views import upload_image

urlpatterns = [
    path('', upload_image, name='home'),  # Redirects '/' to 'upload/'
    path('upload/', upload_image, name='upload_image'),  # Upload page
]
