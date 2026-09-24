from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import translation

from quiz.models import Category, Question, Answer, QuizResult


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name_en="Driving Time",
            name_ro="Timp de conducere",
            slug="driving-time",
        )

    def test_category_is_created(self):
        self.assertEqual(self.category.name_en, "Driving Time")
        self.assertEqual(self.category.name_ro, "Timp de conducere")
        self.assertEqual(self.category.slug, "driving-time")

    def test_category_localized_name_in_english(self):
        with translation.override("en"):
            self.assertEqual(
                self.category.localized_name,
                "Driving Time"
            )

    def test_category_localized_name_in_romanian(self):
        with translation.override("ro"):
            self.assertEqual(
                self.category.localized_name,
                "Timp de conducere"
            )


class QuestionModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name_en="Driving Time",
            name_ro="Timp de conducere",
            slug="driving-time",
        )

        self.question = Question.objects.create(
            category=self.category,
            text_en="What is the maximum daily driving time?",
            text_ro="Care este timpul maxim zilnic de conducere?",
            explanation_en="This is the English explanation.",
            explanation_ro="Aceasta este explicația în limba română.",
        )

    def test_question_belongs_to_category(self):
        self.assertEqual(
            self.question.category,
            self.category
        )

    def test_question_localized_text_in_english(self):
        with translation.override("en"):
            self.assertEqual(
                self.question.localized_text,
                "What is the maximum daily driving time?"
            )

    def test_question_localized_text_in_romanian(self):
        with translation.override("ro"):
            self.assertEqual(
                self.question.localized_text,
                "Care este timpul maxim zilnic de conducere?"
            )

    def test_question_localized_explanation_in_english(self):
        with translation.override("en"):
            self.assertEqual(
                self.question.localized_explanation,
                "This is the English explanation."
            )

    def test_question_localized_explanation_in_romanian(self):
        with translation.override("ro"):
            self.assertEqual(
                self.question.localized_explanation,
                "Aceasta este explicația în limba română."
            )


class AnswerModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name_en="Driving Time",
            name_ro="Timp de conducere",
            slug="driving-time",
        )

        self.question = Question.objects.create(
            category=self.category,
            text_en="What is the maximum daily driving time?",
            text_ro="Care este timpul maxim zilnic de conducere?",
            explanation_en="This is the English explanation.",
            explanation_ro="Aceasta este explicația în limba română.",
        )

        self.answer = Answer.objects.create(
            question=self.question,
            text_en="9 hours",
            text_ro="9 ore",
            is_correct=True,
        )

    def test_answer_belongs_to_question(self):
        self.assertEqual(
            self.answer.question,
            self.question
        )

    def test_answer_is_correct(self):
        self.assertTrue(self.answer.is_correct)

    def test_answer_localized_text_in_english(self):
        with translation.override("en"):
            self.assertEqual(
                self.answer.localized_text,
                "9 hours"
            )

    def test_answer_localized_text_in_romanian(self):
        with translation.override("ro"):
            self.assertEqual(
                self.answer.localized_text,
                "9 ore"
            )



class QuizResultModelTest(TestCase):

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

        self.quiz_result = QuizResult.objects.create(
            user=self.user,
            category=self.category,
            score=8,
            total_questions=10,
        )

    def test_quiz_result_belongs_to_user(self):
        self.assertEqual(
            self.quiz_result.user,
            self.user
        )

    def test_quiz_result_belongs_to_category(self):
        self.assertEqual(
            self.quiz_result.category,
            self.category
        )

    def test_quiz_result_score(self):
        self.assertEqual(
            self.quiz_result.score,
            8
        )

    def test_quiz_result_total_questions(self):
        self.assertEqual(
            self.quiz_result.total_questions,
            10
        )

    def test_quiz_result_string_representation(self):
        self.assertEqual(
            str(self.quiz_result),
            "testuser - Driving Time - 8/10"
        )

    def test_quiz_result_category_becomes_null_when_category_deleted(self):
        self.category.delete()

        self.quiz_result.refresh_from_db()

        self.assertIsNone(self.quiz_result.category)