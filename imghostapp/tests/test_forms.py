from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from imghostapp.forms import ImageForm

class ImageFormTest(TestCase):
    def test_image_form_valid(self):
        file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        form = ImageForm(data={'title': 'Test Image'}, files={'image': file})
        self.assertTrue(form.is_valid())