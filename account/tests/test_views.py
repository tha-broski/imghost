from django.test import TestCase, Client
from django.urls import reverse
from account.models import Account

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user(email='view@example.com', username='viewuser', password='password123')

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('login'), {
            'email': 'view@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.client.login(email='view@example.com', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_upload_image_post_invalid_not_logged_in(self):
        response = self.client.post(reverse('upload-image'))
        self.assertEqual(response.status_code, 302)  # Redirect to login