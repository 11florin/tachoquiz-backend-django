from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/login.html")


    def test_user_can_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpassword123",
            }
        )

        self.assertRedirects(response, reverse("home"))

        self.assertTrue(
            "_auth_user_id" in self.client.session
        )

    def test_user_cannot_login_with_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "wrongpassword",
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "Invalid username or password."
        )

        self.assertFalse(
            "_auth_user_id" in self.client.session
        )


    def test_user_can_logout(self):
        self.client.login(
            username="testuser",
            password="testpassword123",
        )

        response = self.client.get(reverse("logout"))

        self.assertRedirects(response, reverse("home"))

        self.assertFalse(
            "_auth_user_id" in self.client.session
        )

    def test_user_can_register(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
            }
        )

        self.assertRedirects(
            response,
            reverse("confirmation")
        )

        self.assertTrue(
            get_user_model().objects.filter(
                username="newuser"
            ).exists()
        )

    def test_user_cannot_register_with_duplicate_username(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "email": "another@example.com",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            get_user_model().objects.filter(
                username="testuser"
            ).count(),
            1
        )

    def test_unauthenticated_user_cannot_access_quiz(self):
        response = self.client.get(reverse("quiz"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('quiz')}"
        )

    def test_authenticated_user_can_access_quiz(self):
        self.client.login(
            username="testuser",
            password="testpassword123",
        )

        response = self.client.get(reverse("quiz"))

        self.assertRedirects(
            response,
            reverse("categories")
        )

    def test_login_redirects_to_next_url(self):
        response = self.client.post(
            f"{reverse('login')}?next={reverse('quiz')}",
            {
                "username": "testuser",
                "password": "testpassword123",
            }
        )

        self.assertRedirects(
            response,
            reverse("quiz"),
            fetch_redirect_response=False,
        )