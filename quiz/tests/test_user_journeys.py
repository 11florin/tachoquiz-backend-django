from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from quiz.models import Answer, Category, Question, QuizResult


class UserJourneyTest(TestCase):

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
            text_en="What is the daily driving limit?",
            text_ro="Care este limita zilnică de conducere?",
            explanation_en="The normal daily driving limit is 9 hours.",
            explanation_ro="Limita normală zilnică de conducere este de 9 ore.",
        )

        self.correct_answer_one = Answer.objects.create(
            question=self.question_one,
            text_en="9 hours",
            text_ro="9 ore",
            is_correct=True,
        )

        Answer.objects.create(
            question=self.question_one,
            text_en="12 hours",
            text_ro="12 ore",
            is_correct=False,
        )

        self.question_two = Question.objects.create(
            category=self.category,
            text_en="What is the weekly driving limit?",
            text_ro="Care este limita săptămânală de conducere?",
            explanation_en="The weekly driving limit is 56 hours.",
            explanation_ro="Limita săptămânală de conducere este de 56 de ore.",
        )

        self.correct_answer_two = Answer.objects.create(
            question=self.question_two,
            text_en="56 hours",
            text_ro="56 de ore",
            is_correct=True,
        )

        Answer.objects.create(
            question=self.question_two,
            text_en="70 hours",
            text_ro="70 de ore",
            is_correct=False,
        )


    def test_complete_quiz_user_journey(self):
        # 1. User logs in
        login_response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpassword123",
            },
        )

        self.assertRedirects(
            login_response,
            reverse("home"),
        )

        # 2. User opens the categories page
        categories_response = self.client.get(
            reverse("categories")
        )

        self.assertEqual(
            categories_response.status_code,
            200
        )

        # 3. User starts the quiz
        quiz_response = self.client.get(
            reverse(
                "category-quiz",
                kwargs={"slug": self.category.slug},
            )
        )

        self.assertEqual(
            quiz_response.status_code,
            200
        )

        # 4. Find which question Django selected first
        session = self.client.session

        first_question_id = session["quiz_question_ids"][0]

        first_question = Question.objects.get(
            id=first_question_id
        )

        correct_answer = first_question.answers.get(
            is_correct=True
        )

        # 5. User submits the correct answer
        answer_response = self.client.post(
            reverse(
                "category-quiz",
                kwargs={"slug": self.category.slug},
            ),
            {
                "answer": correct_answer.id,
            },
        )

        self.assertRedirects(
            answer_response,
            reverse(
                "category-quiz",
                kwargs={"slug": self.category.slug},
            ),
        )

        # 6. User clicks Next
        next_response = self.client.post(
            reverse(
                "category-quiz",
                kwargs={"slug": self.category.slug},
            ),
            {
                "action": "next",
            },
        )

        self.assertRedirects(
            next_response,
            reverse(
                "category-quiz",
                kwargs={"slug": self.category.slug},
            ),
        )

        # 7. Find the second question
        session = self.client.session

        second_question_id = session["quiz_question_ids"][1]

        second_question = Question.objects.get(
            id=second_question_id
        )

        correct_answer = second_question.answers.get(
            is_correct=True
        )

        # 8. User submits the correct answer
        answer_response = self.client.post(
            reverse(
                "category-quiz",
                kwargs={"slug": self.category.slug},
            ),
            {
                "answer": correct_answer.id,
            },
        )

        self.assertRedirects(
            answer_response,
            reverse(
                "category-quiz",
                kwargs={"slug": self.category.slug},
            ),
        )

        # 9. User finishes the quiz
        finish_response = self.client.post(
            reverse(
                "category-quiz",
                kwargs={"slug": self.category.slug},
            ),
            {
                "action": "next",
            },
        )

        self.assertRedirects(
            finish_response,
            reverse("score"),
        )

        # 10. User opens the score page
        score_response = self.client.get(
            reverse("score")
        )

        self.assertEqual(
            score_response.status_code,
            200
        )

        self.assertEqual(
            score_response.context["correct_answers"],
            2
        )

        self.assertEqual(
            score_response.context["total_questions"],
            2
        )

        self.assertEqual(
            score_response.context["percentage"],
            100
        )