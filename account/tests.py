from django.test import TestCase, Client
from django.urls import reverse
from .models import Account
from .views import RegisterForm


class StartViewTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('start'))

    def test_statis(self):
        self.assertEqual(self.response.status_code, 200)

    def test_html(self):
        self.assertTemplateUsed(self.response, 'account/start.html')


class AccountModelTest(TestCase):
    def setUp(self):
        self.data = {
            'name': 'test',
            'email': 'test@example.com',
            'password': 'password'
        }
        self.account = Account.objects.create(
            name=self.data['name'], email=self.data['email'], password=self.data['password'])

    def test_acount_number(self):
        account_count = Account.objects.count()
        self.assertEqual(account_count, 1)

    def test_account_data(self):
        self.assertEqual(self.data['name'], self.account.name)
        self.assertEqual(self.data['email'], self.account.email)
        self.assertEqual(self.data['password'], self.account.password)


class RegisterViewTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('register'))

    def test_status(self):
        self.assertEqual(self.response.status_code, 200)

    def test_html(self):
        self.assertTemplateUsed(self.response, 'account/register.html')
        # なぜ'account/registerというパスで指定できてるのかは分からない


class RegisterTests(TestCase):
    def setUp(self):
        self.assertEqual(Account.objects.count(), 0)
        self.url = reverse('register')
        self.start_url = reverse('start')
        self.data = {
            'name': 'test',
            'email': 'test@register.com',
            'password': 'password'
        }
        self.response = self.client.post(self.url, self.data)

    def test_account(self):
        self.assertEqual(Account.objects.count(), 1)
        self.assertRedirects(self.response, self.start_url)


class RegisterErrorTests(TestCase):
    def setUp(self):
        self.url = reverse('register')
        self.data = {
            'name': 'test',
            'email': 'test@register.com',
            'password': 'password'
        }

    def test_data_empty(self):
        data = {}
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')

    def test_short_password(self):
        # 8文字未満のパスワードを受け付けない
        self.data['password'] = '1234567'
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')

    def test_too_long_name(self):
        # 31文字以上の名前を受け付けない
        self.data['name'] = "1234567890123456789012345678901"
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')

    def test_error_email(self):
        # 不適切なメールアドレスを受け付けない
        self.data['email'] = 'test'
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')
