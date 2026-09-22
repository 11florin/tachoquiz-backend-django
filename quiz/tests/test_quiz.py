from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from quiz.models import Answer, Category, Question


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
        self.second_question = Question.objects.create(
            category=self.category,
            text_en="What is the normal weekly driving limit?",
            text_ro="Care este limita normală săptămânală de conducere?",
            explanation_en="Test explanation.",
            explanation_ro="Explicație de test.",
        )

        self.second_question_answer = Answer.objects.create(
            question=self.second_question,
            text_en="56 hours",
            text_ro="56 de ore",
            is_correct=True,
        )

        self.second_question_wrong_answer = Answer.objects.create(
            question=self.second_question,
            text_en="60 hours",
            text_ro="60 de ore",
            is_correct=False,
        )

        self.answer = Answer.objects.create(
            question=self.question,
            text_en="9 hours",
            text_ro="9 ore",
            is_correct=True,
        )

        self.second_answer = Answer.objects.create(
            question=self.question,
            text_en="10 hours",
            text_ro="10 ore",
            is_correct=False,
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

        session = self.client.session

        first_question_id = session["quiz_question_ids"][0]

        self.assertEqual(
            response.context["question"].id,
            first_question_id
        )

        self.assertEqual(
            response.context["question_number"],
            1
        )

        self.assertEqual(
            response.context["total_questions"],
            2
        )

    def test_selected_answer_is_saved_in_session(self):
        quiz_url = reverse(
            "category-quiz",
            kwargs={"slug": self.category.slug},
        )

        # Start the quiz.
        self.client.get(quiz_url)

        session = self.client.session

        # Find which question was randomly selected first.
        first_question_id = session["quiz_question_ids"][0]

        first_question = Question.objects.get(
            id=first_question_id
        )

        first_answer = first_question.answers.first()

        # Submit an answer belonging to the current question.
        response = self.client.post(
            quiz_url,
            {
                "answer": first_answer.id,
            }
        )

        self.assertRedirects(
            response,
            quiz_url
        )

        session = self.client.session

        self.assertEqual(
            session["quiz_answers"][str(first_question.id)],
            str(first_answer.id),
        )

    def test_answer_cannot_be_changed_after_submission(self):
        quiz_url = reverse(
            "category-quiz",
            kwargs={"slug": self.category.slug},
        )

        # Start the quiz.
        self.client.get(quiz_url)

        session = self.client.session

        first_question_id = session["quiz_question_ids"][0]

        first_question = Question.objects.get(
            id=first_question_id
        )

        answers = list(first_question.answers.all())

        first_answer = answers[0]
        second_answer = answers[1]

        # Submit the first answer.
        self.client.post(
            quiz_url,
            {
                "answer": first_answer.id,
            }
        )

        # Try to change it.
        self.client.post(
            quiz_url,
            {
                "answer": second_answer.id,
            }
        )

        session = self.client.session

        self.assertEqual(
            session["quiz_answers"][str(first_question.id)],
            str(first_answer.id),
        )

    def test_next_moves_to_next_question(self):
        quiz_url = reverse(
            "category-quiz",
            kwargs={"slug": self.category.slug},
        )

        # Start the quiz.
        self.client.get(quiz_url)

        session = self.client.session

        # Find which question Django randomly selected first.
        first_question_id = session["quiz_question_ids"][0]

        first_question = Question.objects.get(
            id=first_question_id
        )

        first_answer = first_question.answers.first()

        # Answer the first question.
        self.client.post(
            quiz_url,
            {
                "answer": first_answer.id,
            }
        )

        # Click Next.
        response = self.client.post(
            quiz_url,
            {
                "action": "next",
            }
        )

        self.assertRedirects(
            response,
            quiz_url
        )

        session = self.client.session

        self.assertEqual(
            session["question_index"],
            1
        )


    def test_completing_all_questions_redirects_to_score(self):
        quiz_url = reverse(
            "category-quiz",
            kwargs={"slug": self.category.slug},
        )

        # Start the quiz.
        self.client.get(quiz_url)

        # Answer every question in the order stored in the session.
        for _ in range(2):
            session = self.client.session

            question_index = session["question_index"]
            question_ids = session["quiz_question_ids"]

            current_question_id = question_ids[question_index]

            current_question = Question.objects.get(
                id=current_question_id
            )

            answer = current_question.answers.first()

            # Submit an answer.
            self.client.post(
                quiz_url,
                {
                    "answer": answer.id,
                }
            )

            # Move to the next question.
            response = self.client.post(
                quiz_url,
                {
                    "action": "next",
                }
            )

        self.assertRedirects(
            response,
            reverse("score")
        )

        session = self.client.session

        self.assertTrue(
            session["quiz_complete"]
        )

    def test_next_does_not_advance_without_answer(self):
        quiz_url = reverse(
            "category-quiz",
            kwargs={"slug": self.category.slug},
        )

        # Start the quiz.
        self.client.get(quiz_url)

        # Try to click Next without answering.
        response = self.client.post(
            quiz_url,
            {
                "action": "next",
            }
        )

        self.assertRedirects(
            response,
            quiz_url
        )

        session = self.client.session

        self.assertEqual(
            session["question_index"],
            0
        )

    def test_category_without_questions_redirects_to_categories(self):
        empty_category = Category.objects.create(
            name_en="Empty Category",
            name_ro="Categorie goală",
            slug="empty-category",
        )

        response = self.client.get(
            reverse(
                "category-quiz",
                kwargs={"slug": empty_category.slug},
            )
        )

        self.assertRedirects(
            response,
            reverse("categories")
        )