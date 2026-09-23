from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from quiz.models import Category, QuizResult


class QuizResultsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        self.other_user = get_user_model().objects.create_user(
            username="otheruser",
            password="otherpassword123",
        )

        self.category = Category.objects.create(
            name_en="Driving Time",
            name_ro="Timp de conducere",
            slug="driving-time",
        )

        self.user_result = QuizResult.objects.create(
            user=self.user,
            category=self.category,
            score=8,
            total_questions=10,
        )

        self.other_user_result = QuizResult.objects.create(
            user=self.other_user,
            category=self.category,
            score=5,
            total_questions=10,
        )

        self.client.login(
            username="testuser",
            password="testpassword123",
        )

    def test_user_sees_only_their_own_results(self):
        response = self.client.get(
            reverse("quiz-history")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "quiz/quiz_history.html"
        )

        self.assertContains(
            response,
            "8 / 10"
        )

        self.assertNotContains(
            response,
            "5 / 10"
        )

    def test_unauthenticated_user_cannot_access_quiz_history(self):
        self.client.logout()

        response = self.client.get(
            reverse("quiz-history")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('quiz-history')}"
        )

    def test_user_with_no_results_can_access_quiz_history(self):
        user_without_results = get_user_model().objects.create_user(
            username="newuser",
            password="newpassword123",
        )

        self.client.logout()

        self.client.login(
            username="newuser",
            password="newpassword123",
        )

        response = self.client.get(
            reverse("quiz-history")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "quiz/quiz_history.html"
        )

        self.assertEqual(
            response.context["results"].count(),
            0
        )

    def test_quiz_history_contains_only_current_user_results(self):
        response = self.client.get(
            reverse("quiz-history")
        )

        results = response.context["results"]

        self.assertIn(
            self.user_result,
            results
        )

        self.assertNotIn(
            self.other_user_result,
            results
        )