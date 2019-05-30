from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from account.models import User


class BaseTestCase(TestCase):

    def setUp(self):
        self.username = 'test_username'
        self.password = User.objects.make_random_password()
        self.user = User.objects.create_user(self.username, password=self.password)

    def login(self, client: Client, username: str, password: str) -> JsonResponse:
        return client.post(
            reverse('login'),
            dict(username=self.username, password=self.password),
            content_type="application/json",
        )


class LoginViewTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_login_response_json(self):
        c = Client()
        resp = self.login(c, self.username, self.password)
        self.assertIsInstance(resp, JsonResponse)
        self.assertDictEqual(resp.json(), dict(status='success'))



class LogoutViewTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_logout_without_login(self):
        c = Client()
        resp = c.get(reverse('logout'))
        self.assertIsInstance(resp, JsonResponse)
        self.assertDictEqual(resp.json(), dict(status='error', message='not login'))

    def test_logout(self):
        # login
        c = Client()
        self.login(c, self.username, self.password)
        # logout
        resp = c.get(reverse('logout'))
        self.assertIsInstance(resp, JsonResponse)
        self.assertDictEqual(resp.json(), dict(status='success'))


class GetUserInfoTestCase(BaseTestCase):

    def setUp(self):
        return super().setUp()

    def test_get_user_info(self):
        # login
        c = Client()
        self.login(c, self.username, self.password)
        resp = c.get(reverse('get_user_info'))
        self.assertIsInstance(resp, JsonResponse)
        data = resp.json()
        self.assertEqual(data['status'], 'success')


class LoginPageViewTestCase(BaseTestCase):

    def setUp(self):
        return super().setUp()

    def test_get_login_page(self):
        c = Client()
        resp = c.get(reverse('login_page'))
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(resp.status_code, 200)


class UserPageViewTestCase(BaseTestCase):

    def setUp(self):
        return super().setUp()

    def test_get_user_page_without_login(self):
        # login
        c = Client()
        # self.login(c, self.username, self.password)
        resp = c.get(reverse('user_page'))
        self.assertIsInstance(resp, HttpResponse)
        self.assertRedirects(
            resp,
            reverse('login_page'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_get_user_page_after_login(self):
        # login
        c = Client()
        self.login(c, self.username, self.password)
        resp = c.get(reverse('user_page'))
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(resp.status_code, 200)
