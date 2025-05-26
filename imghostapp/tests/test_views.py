from django.test import TestCase, Client
from django.urls import reverse
from account.models import Account
from imghostapp.models import Image
from django.core.files.uploadedfile import SimpleUploadedFile

class ImghostViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user(email='view@example.com', username='viewuser', password='password123')
        self.client.login(email='view@example.com', password='password123')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imghostapp/home.html')

    def test_upload_image_get(self):
        response = self.client.get(reverse('upload-image'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imghostapp/upload.html')

    def test_upload_image_post_valid(self):
        file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(reverse('upload-image'), {'title': 'Uploaded Image', 'image': file})
        self.assertEqual(response.status_code, 200) 

    def test_user_gallery_access(self):
        response = self.client.get(reverse('user_gallery', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery/user_gallery.html')

    def test_delete_image(self):
        image = Image.objects.create(title='To Delete', user=self.user, image='somepath.jpg')
        response = self.client.post(reverse('delete_image', args=[image.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Image.objects.filter(id=image.id).exists())

    def test_edit_image_get(self):
        image = Image.objects.create(title='Editable', user=self.user, image='somepath.jpg')
        response = self.client.get(reverse('edit_image', args=[image.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery/edit_image.html')

    def test_edit_image_post(self):
        image = Image.objects.create(title='Old Title', user=self.user, image='somepath.jpg')
        response = self.client.post(reverse('edit_image', args=[image.id]), {'title': 'New Title'})
        self.assertEqual(response.status_code, 302)
        image.refresh_from_db()
        self.assertEqual(image.title, 'New Title')

    def test_user_gallery_forbidden_access(self):
        other_user = Account.objects.create_user(email='other@example.com', username='otheruser', password='password123')
        self.client.logout()
        self.client.login(email='other@example.com', password='password123')
        response = self.client.get(reverse('user_gallery', args=[self.user.username]))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_download_image(self):
        image_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        image = Image.objects.create(title="Test Image", user=self.user, image=image_file)

        url = reverse('download_image', args=[image.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('attachment', response.get('Content-Disposition'))

        content = b''.join(response.streaming_content)
        self.assertEqual(content, b"file_content")
