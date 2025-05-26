import os
import shutil
import tempfile
from django.test import TestCase
from django.conf import settings
from account.models import Account
from imghostapp.models import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PilImage
import io

class SignalTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(email='signal@example.com', username='signaluser', password='testpass123')
        self.temp_dir = tempfile.mkdtemp()
        self.original_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = self.temp_dir

        image_io = io.BytesIO()
        image = PilImage.new('RGB', (100, 100), color='red')
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        uploaded_file = SimpleUploadedFile("image.jpg", image_io.read(), content_type="image/jpeg")

        self.image = Image.objects.create(title='Signal Image', user=self.user, image=uploaded_file)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        settings.MEDIA_ROOT = self.original_media_root

    def test_image_file_deleted_on_model_delete(self):
        image_path = self.image.image.path
        self.assertTrue(os.path.exists(image_path))
        self.image.delete()
        self.assertFalse(os.path.exists(image_path))