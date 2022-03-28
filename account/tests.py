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
            'username': 'test',
            'email': 'test@example.com',
            'password': 'test.password'
        }
        self.account = Account.objects.create(
            username=self.data['username'], email=self.data['email'], password=self.data['password'])

    def test_acount_number(self):
        account_count = Account.objects.count()
        self.assertEqual(account_count, 1)

    def test_account_data(self):
        self.assertEqual(self.data['username'], self.account.username)
        self.assertEqual(self.data['email'], self.account.email)
        self.assertEqual(self.data['password'], self.account.password)


class RegisterViewTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('register'))

    def test_status(self):
        self.assertEqual(self.response.status_code, 200)

    def test_html(self):
        self.assertTemplateUsed(self.response, 'account/register.html')


class RegisterTests(TestCase):
    def setUp(self):
        self.assertEqual(Account.objects.count(), 0)
        self.url = reverse('register')
        self.start_url = reverse('start')
        self.data = {
            'username': 'test',
            'email': 'test@example.com',
            'password1': 'test.password',
            'password2': 'test.password',
        }
        self.response = self.client.post(self.url, self.data)

    def test_account(self):
        self.assertEqual(Account.objects.count(), 1)
        self.assertRedirects(self.response, self.start_url)


class RegisterErrorTests(TestCase):
    def setUp(self):
        self.url = reverse('register')
        self.data = {
            'username': 'test',
            'email': 'test@register.com',
            'password1': 'test.password',
            'password2': 'test.password',
        }

    def test_data_empty(self):
        data = {}
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')

    def test_short_password(self):
        # 8文字未満のパスワードを受け付けない
        self.data['password1'] = 'abcd123'
        self.data['password2'] = 'abcd123'
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')

    def test_only_number_password(self):
        # 数字だけのパスワードを受け付けない
        self.data['password1'] = '12345678'
        self.data['password2'] = '12345678'
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')

    def test_not_equal_password(self):
        # 異なるパスワードを受け付けない
        self.data['password2'] = 'test.password2'
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')

    def test_blank_username(self):
        # 空白のパスワードを受け付けない
        self.data['password1'] = ''
        self.data['password2'] = ''
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')

    def test_blank_username(self):
        # 空白のユーザ名を受け付けない
        self.data['username'] = ''
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')

    def test_same_username(self):
        # 既に登録されているユーザ名を受け付けない
        self.response = self.client.post(self.url, self.data)
        same_name_data = {
            'username': 'test',
            'email': 'test1@register.com',
            'password1': 'test1.password',
            'password2': 'test1.password',
        }
        self.response = self.client.post(self.url, same_name_data)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(Account.objects.count(), 1)
        self.assertTemplateUsed(self.response, 'account/register.html')

    def test_error_email(self):
        # 不適切なメールアドレスを受け付けない
        self.data['email'] = 'test'
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')

    def test_blank_username(self):
        # 空白のメールアドレスを受け付けない
        self.data['email'] = ''
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Account.objects.exists())
        self.assertTemplateUsed(self.response, 'account/register.html')
