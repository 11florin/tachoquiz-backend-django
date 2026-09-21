from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from quiz.models import Category, Question


class QuizFunctionalityTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        self.category = Category.objects.create(
            name_en="Driving Time",
            name_ro="Timp de conducere",
            slug="driving-time",
        )

        self.question = Question.objects.create(
            category=self.category,
            text_en="What is the maximum daily driving time?",
            text_ro="Care este timpul maxim zilnic de conducere?",
            explanation_en="Test explanation.",
            explanation_ro="Explicație de test.",
        )

        self.client.login(
            username="testuser",
            password="testpassword123",
        )

    def test_starting_quiz_creates_quiz_session(self):
        response = self.client.get(
            reverse(
                "category-quiz",
                kwargs={"slug": self.category.slug},
            )
        )

        self.assertEqual(response.status_code, 200)

        session = self.client.session

        self.assertEqual(
            session["quiz_category_id"],
            self.category.id
        )

        self.assertEqual(
            session["question_index"],
            0
        )

        self.assertEqual(
            session["quiz_answers"],
            {}
        )

        self.assertFalse(
            session["quiz_complete"]
        )

        self.assertFalse(
            session["quiz_result_saved"]
        )

    def test_quiz_session_contains_category_questions(self):
        self.client.get(
            reverse(
                "category-quiz",
                kwargs={"slug": self.category.slug},
            )
        )

        session = self.client.session

        self.assertIn(
            self.question.id,
            session["quiz_question_ids"]
        )

    def test_first_question_is_displayed(self):
        response = self.client.get(
            reverse(
                "category-quiz",
                kwargs={"slug": self.category.slug},
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "quiz/quiz.html"
        )

        self.assertEqual(
            response.context["question"],
            self.question
        )

        self.assertEqual(
            response.context["question_number"],
            1
        )

        self.assertEqual(
            response.context["total_questions"],
            1
        )