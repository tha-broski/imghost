from django.test import TestCase
from account.forms import AccountAuthenticationForm
from account.models import Account

class AccountAuthenticationFormTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(email='login@example.com', username='loginuser', password='testpass123')

    def test_authentication_form_valid(self):
        form = AccountAuthenticationForm(data={
            'email': 'login@example.com',
            'password': 'testpass123'
        })
        self.assertTrue(form.is_valid())

    def test_authentication_form_invalid(self):
        form = AccountAuthenticationForm(data={
            'email': 'login@example.com',
            'password': 'wrongpass'
        })
        self.assertFalse(form.is_valid())