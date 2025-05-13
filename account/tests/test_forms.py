from django.test import TestCase
from account.forms import RegistrationForm
from account.models import Account

class RegistrationFormTest(TestCase):
    def test_registration_form_valid_data(self):
        form = RegistrationForm(data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        self.assertTrue(form.is_valid())

    def test_registration_form_duplicate_email(self):
        Account.objects.create_user(email='test@example.com', username='user1', password='testpass123')
        form = RegistrationForm(data={
            'email': 'test@example.com',
            'username': 'user2',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_registration_form_duplicate_username(self):
        Account.objects.create_user(email='test2@example.com', username='testuser', password='testpass123')
        form = RegistrationForm(data={
            'email': 'new@example.com',
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)