from django.test import TestCase
from account.models import Account

class AccountModelTest(TestCase):
    def test_create_user(self):
        user = Account.objects.create_user(email='user@example.com', username='user', password='pass123')
        self.assertEqual(user.email, 'user@example.com')
        self.assertFalse(user.is_admin)

    def test_create_superuser(self):
        admin = Account.objects.create_superuser(email='admin@example.com', username='admin', password='adminpass')
        self.assertTrue(admin.is_admin)
        self.assertTrue(admin.is_superuser)