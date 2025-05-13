import os
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from imghostapp.models import Image
from django.contrib.auth import get_user_model
import tempfile

User = get_user_model()

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class SignalTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(email="test2@example.com", username="user2", password="pass")

        # Create image instance with actual file
        self.image_file = SimpleUploadedFile("testimage.jpg", b"file_content", content_type="image/jpeg")
        self.image = Image.objects.create(title="Test Image", image=self.image_file, user=self.user)

        self.image_path = self.image.image.path

        # Confirm file exists
        self.assertTrue(os.path.isfile(self.image_path))

    def test_image_file_deleted_on_instance_delete(self):
        self.image.delete()
        self.assertFalse(os.path.isfile(self.image_path))
