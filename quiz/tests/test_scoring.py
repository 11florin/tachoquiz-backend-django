from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from quiz.models import Answer, Category, Question, QuizResult


class QuizScoringTest(TestCase):

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

        self.question_one = Question.objects.create(
            category=self.category,
            text_en="Question one",
            text_ro="Întrebarea unu",
            explanation_en="Explanation one",
            explanation_ro="Explicația unu",
        )

        self.correct_answer_one = Answer.objects.create(
            question=self.question_one,
            text_en="Correct answer",
            text_ro="Răspuns corect",
            is_correct=True,
        )

        self.wrong_answer_one = Answer.objects.create(
            question=self.question_one,
            text_en="Wrong answer",
            text_ro="Răspuns greșit",
            is_correct=False,
        )

        self.question_two = Question.objects.create(
            category=self.category,
            text_en="Question two",
            text_ro="Întrebarea doi",
            explanation_en="Explanation two",
            explanation_ro="Explicația doi",
        )

        self.correct_answer_two = Answer.objects.create(
            question=self.question_two,
            text_en="Correct answer",
            text_ro="Răspuns corect",
            is_correct=True,
        )

        self.wrong_answer_two = Answer.objects.create(
            question=self.question_two,
            text_en="Wrong answer",
            text_ro="Răspuns greșit",
            is_correct=False,
        )

        self.client.login(
            username="testuser",
            password="testpassword123",
        )

    def test_score_with_all_correct_answers(self):
        session = self.client.session

        session["quiz_question_ids"] = [
            self.question_one.id,
            self.question_two.id,
        ]

        session["quiz_answers"] = {
            str(self.question_one.id): str(self.correct_answer_one.id),
            str(self.question_two.id): str(self.correct_answer_two.id),
        }

        session["quiz_complete"] = True
        session["quiz_category_id"] = self.category.id
        session["quiz_result_saved"] = False

        session.save()

        response = self.client.get(
            reverse("score")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.context["correct_answers"],
            2
        )

        self.assertEqual(
            response.context["incorrect_answers"],
            0
        )

        self.assertEqual(
            response.context["total_questions"],
            2
        )

        self.assertEqual(
            response.context["percentage"],
            100
        )

    def test_score_with_one_correct_and_one_wrong_answer(self):
        session = self.client.session

        session["quiz_question_ids"] = [
            self.question_one.id,
            self.question_two.id,
        ]

        session["quiz_answers"] = {
            str(self.question_one.id): str(self.correct_answer_one.id),
            str(self.question_two.id): str(self.wrong_answer_two.id),
        }

        session["quiz_complete"] = True
        session["quiz_category_id"] = self.category.id
        session["quiz_result_saved"] = False

        session.save()

        response = self.client.get(
            reverse("score")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.context["correct_answers"],
            1
        )

        self.assertEqual(
            response.context["incorrect_answers"],
            1
        )

        self.assertEqual(
            response.context["total_questions"],
            2
        )

        self.assertEqual(
            response.context["percentage"],
            50
        )