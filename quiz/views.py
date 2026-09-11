from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from .forms import RegistrationForm
from .models import Category, Question, Answer, QuizResult



def home(request):
    """Render the home page."""
    return render(request, "quiz/home.html")


def register(request):
    """Register a new user and redirect successful registrations."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("confirmation")

    else:
        form = RegistrationForm()

    return render(request, "quiz/register.html", {"form": form})


def confirmation(request):
    """Render the registration confirmation page."""
    return render(request, "quiz/confirmation.html")



def login_view(request):
    """Authenticate a user and start a login session."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            return redirect("home")

        return render(request, "quiz/login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "quiz/login.html")



def logout_view(request):
    """Log out the current user and redirect to the home page."""
    logout(request)
    messages.success(request, "You've been logged out successfully.")
    return redirect("home")


@login_required
def quiz_view(request):
    """Redirect authenticated users to the quiz categories page."""
    return redirect("categories")


@login_required
def score_view(request):
    """Calculate and display the completed quiz score."""

    quiz_answers = request.session.get("quiz_answers", {})
    question_ids = request.session.get("quiz_question_ids", [])
    quiz_complete = request.session.get("quiz_complete", False)

    if not quiz_complete or not question_ids:
        messages.error(
            request,
            "No completed quiz was found. Please start a new quiz."
        )
        return redirect("categories")

    selected_answer_ids = list(quiz_answers.values())

    correct_answers = Answer.objects.filter(
        id__in=selected_answer_ids,
        is_correct=True,
    ).count()

    total_questions = len(question_ids)
    incorrect_answers = total_questions - correct_answers

    percentage = (
        round((correct_answers / total_questions) * 100)
        if total_questions
        else 0
    )

    quiz_result_saved = request.session.get(
    "quiz_result_saved",
    False,
)

    if not quiz_result_saved:
        category_id = request.session.get("quiz_category_id")

        category = get_object_or_404(
            Category,
            id=category_id,
        )

        QuizResult.objects.create(
            user=request.user,
            category=category,
            score=correct_answers,
            total_questions=total_questions,
        )

        request.session["quiz_result_saved"] = True

    context = {
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "total_questions": total_questions,
        "percentage": percentage,
    }

    return render(request, "quiz/score.html", context)


@login_required
def categories(request):
    """Display quiz categories and their number of questions."""
    categories = Category.objects.annotate(
        question_count=Count("questions")
    )

    return render(
        request,
        "quiz/categories.html",
        {"categories": categories},
    )


@login_required
def category_quiz(request, slug):
    """
    Start a category quiz and manage progression through its questions.

    Questions are randomized when the quiz starts and their IDs are
    stored in the user's session to maintain the quiz order.
    """
    category = get_object_or_404(Category, slug=slug)

    active_category_id = request.session.get("quiz_category_id")
    quiz_complete = request.session.get("quiz_complete", False)

    # Start a new quiz if there is no active quiz for this category,
    # or if the previous quiz has already been completed.
    if request.method == "GET" and (
        active_category_id != category.id or quiz_complete
    ):
        question_ids = list(
            category.questions.order_by("?").values_list("id", flat=True)
        )

        if not question_ids:
            messages.info(
                request,
                "No questions available for this category."
            )
            return redirect("categories")

        request.session["quiz_category_id"] = category.id
        request.session["quiz_question_ids"] = question_ids
        request.session["question_index"] = 0
        request.session["quiz_answers"] = {}
        request.session["quiz_complete"] = False
        request.session["quiz_result_saved"] = False

    question_ids = request.session.get("quiz_question_ids", [])
    question_index = request.session.get("question_index", 0)

    if not question_ids:
        messages.error(
            request,
            "Quiz session expired. Please start the quiz again."
        )
        return redirect("categories")

    if request.session.get("quiz_category_id") != category.id:
        messages.error(
            request,
            "Quiz session expired. Please start the quiz again."
        )
        return redirect("categories")

    if question_index >= len(question_ids):
        return redirect("score")

    question = get_object_or_404(
        Question,
        id=question_ids[question_index],
        category=category,
    )

    quiz_answers = request.session.get("quiz_answers", {})
    saved_answer_id = quiz_answers.get(str(question.id))

    selected_answer = None

    if saved_answer_id:
        selected_answer = Answer.objects.filter(
            id=saved_answer_id,
            question=question,
        ).first()

    correct_answer = question.answers.filter(
        is_correct=True
    ).first()

    if request.method == "POST":
        action = request.POST.get("action")

        # Move to the next question only after the current
        # question has already been answered.
        if action == "next":
            if selected_answer is None:
                messages.error(
                    request,
                    "Please answer the question before continuing."
                )
                return redirect("category-quiz", slug=slug)

            question_index += 1
            request.session["question_index"] = question_index

            if question_index >= len(question_ids):
                quiz_answers = request.session.get("quiz_answers", {})

                if len(quiz_answers) != len(question_ids):
                    messages.error(
                        request,
                        "Please answer all questions before submitting the quiz."
                    )
                    return redirect("categories")

                request.session["quiz_complete"] = True
                return redirect("score")

            return redirect("category-quiz", slug=slug)

        # Do not allow an already answered question
        # to be answered again.
        if selected_answer is not None:
            return redirect("category-quiz", slug=slug)

        answer_id = request.POST.get("answer")

        if not answer_id:
            return render(
                request,
                "quiz/quiz.html",
                {
                    "category": category,
                    "question": question,
                    "question_number": question_index + 1,
                    "total_questions": len(question_ids),
                    "is_last_question": (
                        question_index == len(question_ids) - 1
                    ),
                    "error": "Please select an answer.",
                },
            )

        answer = Answer.objects.filter(
            id=answer_id,
            question=question,
        ).first()

        if answer is None:
            return render(
                request,
                "quiz/quiz.html",
                {
                    "category": category,
                    "question": question,
                    "question_number": question_index + 1,
                    "total_questions": len(question_ids),
                    "is_last_question": (
                        question_index == len(question_ids) - 1
                    ),
                    "error": "Invalid answer selected.",
                },
            )

        quiz_answers[str(question.id)] = str(answer.id)
        request.session["quiz_answers"] = quiz_answers

        return redirect("category-quiz", slug=slug)

    return render(
        request,
        "quiz/quiz.html",
        {
            "category": category,
            "question": question,
            "question_number": question_index + 1,
            "total_questions": len(question_ids),
            "is_last_question": (
                question_index == len(question_ids) - 1
            ),
            "selected_answer": selected_answer,
            "correct_answer": correct_answer,
        },
    )