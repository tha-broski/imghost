from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from imghostapp.forms import ImageForm
from PIL import Image as PilImage
import io

class ImageFormTest(TestCase):
    def test_image_form_valid(self):

        image_io = io.BytesIO()
        image = PilImage.new('RGB', (100, 100), color='red')
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        file = SimpleUploadedFile("test.jpg", image_io.read(), content_type="image/jpeg")
        form = ImageForm(data={'title': 'Test Image'}, files={'image': file})
        self.assertTrue(form.is_valid())