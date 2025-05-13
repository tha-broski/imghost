import os
import shutil
import tempfile
from django.test import TestCase
from django.conf import settings
from account.models import Account
from imghostapp.models import Image

class SignalTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(email='signal@example.com', username='signaluser', password='testpass123')
        self.temp_dir = tempfile.mkdtemp()
        self.original_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = self.temp_dir

        self.user_folder = os.path.join(settings.MEDIA_ROOT, f'user_{self.user.username}')
        os.makedirs(self.user_folder, exist_ok=True)

        self.test_image_path = os.path.join(self.user_folder, 'image.jpg')
        with open(self.test_image_path, 'wb') as f:
            f.write(b'imagecontent')

        self.image = Image.objects.create(title='Signal Image', user=self.user, image=f'user_{self.user.username}/image.jpg')

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        settings.MEDIA_ROOT = self.original_media_root

    def test_image_file_deleted_on_model_delete(self):
        image_path = self.image.image.path
        self.assertTrue(os.path.exists(image_path))
        self.image.delete()
        self.assertFalse(os.path.exists(image_path))