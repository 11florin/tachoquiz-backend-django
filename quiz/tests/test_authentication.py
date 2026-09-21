from django.test import TestCase
from django.urls import reverse


class AuthenticationTest(TestCase):

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/login.html")