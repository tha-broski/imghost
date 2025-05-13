import os
import shutil
import tempfile
from django.test import TestCase
from django.conf import settings
from django.utils import timezone
from account.models import Account
from imghostapp.models import Image

class ImageModelTest(TestCase):

    def setUp(self):
        # Creates a user for testing
        self.user = Account.objects.create_user(email='testuser@example.com', username='testuser', password='password123')
        
        # Creates a temporary directory to store uploaded files
        self.temp_dir = tempfile.mkdtemp()
        self.original_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = self.temp_dir

        # Creates a directory for the user
        self.user_folder = os.path.join(settings.MEDIA_ROOT, f'user_{self.user.username}')
        os.makedirs(self.user_folder, exist_ok=True)

        # Creates a test image file in the user's directory
        self.test_image_path = os.path.join(self.user_folder, 'test_image.jpg')
        with open(self.test_image_path, 'wb') as f:
            f.write(b'test_image_content')  # Creates the image with sample content

        # Creates an Image object associated with the user
        self.image = Image.objects.create(title='Test Image', user=self.user, image=f'user_{self.user.username}/test_image.jpg')

    def tearDown(self):
        # Deletes the temporary directory and restores the original MEDIA_ROOT
        shutil.rmtree(self.temp_dir)
        settings.MEDIA_ROOT = self.original_media_root

    def test_image_model_creation(self):
        # Test if the image object was created successfully
        self.assertEqual(self.image.title, 'Test Image')
        self.assertEqual(self.image.user, self.user)
        self.assertTrue(os.path.exists(self.image.image.path))  # Checks if the image file exists

    def test_user_directory_path(self):
        # Test if the file path is correct based on the user
        expected_path = f'user_{self.user.username}/test_image.jpg'
        self.assertEqual(self.image.image.name, expected_path)

    def test_image_str_method(self):
        # Test the __str__ method of the Image model
        self.assertEqual(str(self.image), 'Test Image')

