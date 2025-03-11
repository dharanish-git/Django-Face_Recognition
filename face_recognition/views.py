import os
from django.conf import settings
from django.shortcuts import render
from .forms import ImageUploadForm
from .models import UploadedImage
from deepface import DeepFace

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            image_path = image_instance.image.path
            uploaded_image_url = image_instance.image.url  # URL for uploaded image

            db_path = os.path.join(settings.MEDIA_ROOT, "face_database")

            if not os.path.exists(db_path):  # Handle missing database folder
                return render(request, 'result.html', {
                    'name': "Error: face_database/ does not exist!",
                    'uploaded_image': uploaded_image_url,
                    'recognized_image': None
                })

            try:
                # Perform face recognition
                result = DeepFace.find(img_path=image_path, db_path=db_path, model_name="Facenet")

                if not result[0].empty:
                    recognized_path = result[0]['identity'].values[0]  # Full file path
                    recognized_name = os.path.basename(recognized_path).split('.')[0]  # Extract name
                    recognized_image_url = settings.MEDIA_URL + "face_database/" + os.path.basename(recognized_path)
                else:
                    recognized_name = "Unknown Person"
                    recognized_image_url = None

            except Exception as e:
                recognized_name = "Face Couldn't be detected,please Upload an Valid Image!"
                recognized_image_url = None

            return render(request, 'result.html', {
                'name': recognized_name,
                'uploaded_image': uploaded_image_url,
                'recognized_image': recognized_image_url
            })
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})