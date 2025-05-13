import os
import tempfile
from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from imghostapp.utils.storage import get_user_storage_size, get_user_storage_limit

User = get_user_model()

class UtilsTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(email="test@example.com", username="testuser", password="password123")

        # Create user-specific media folder
        self.user_folder = os.path.join(settings.MEDIA_ROOT, f'user_{self.user.username}')
        os.makedirs(self.user_folder, exist_ok=True)

        # Create test files in the user's folder
        self.test_file_path = os.path.join(self.user_folder, "testfile.txt")
        with open(self.test_file_path, 'wb') as f:
            f.write(b"a" * 1024)  # 1KB file

    def tearDown(self):
        # Clean up the test directory
        if os.path.exists(self.user_folder):
            for f in os.listdir(self.user_folder):
                os.remove(os.path.join(self.user_folder, f))
            os.rmdir(self.user_folder)

    def test_get_user_storage_size(self):
        size = get_user_storage_size(self.user)
        self.assertEqual(size, 1024)  # 1KB = 1024 bytes

    def test_get_user_storage_limit_standard_user(self):
        self.assertEqual(get_user_storage_limit(self.user), 5 * 1024 ** 3)

    def test_get_user_storage_limit_premium_user(self):
        self.user.is_premiumuser = True
        self.user.save()
        self.assertEqual(get_user_storage_limit(self.user), 15 * 1024 ** 3)