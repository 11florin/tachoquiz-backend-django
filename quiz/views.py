from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from .forms import RegistrationForm
from .models import Category, Question, Answer



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
    """Render the main quiz page for an authenticated user."""
    return render(request, "quiz/quiz.html")


@login_required
def score_view(request):
    """Render the quiz score page."""
    return render(request, "quiz/score.html")


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

    if request.method == "GET":
        question_ids = list(
            category.questions.order_by("?").values_list("id", flat=True)
        )

        if not question_ids:
            messages.info(
                request,
                "No questions available for this category."
            )
            return redirect("categories")

        request.session["quiz_question_ids"] = question_ids
        request.session["question_index"] = 0
        request.session["quiz_answers"] = {}

    question_ids = request.session.get("quiz_question_ids", [])
    question_index = request.session.get("question_index", 0)

    if question_index >= len(question_ids):
        return redirect("score")

    question = get_object_or_404(
        Question,
        id=question_ids[question_index],
        category=category,
    )

    if request.method == "POST":
        answer_id = request.POST.get("answer")

        if not answer_id:
            return render(
                request,
                "quiz/quiz.html",
                {
                    "category": category,
                    "question": question,
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
                    "error": "Invalid answer selected.",
                },
            )

        quiz_answers = request.session.get("quiz_answers", {})
        quiz_answers[str(question.id)] = str(answer.id)
        request.session["quiz_answers"] = quiz_answers

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

            return redirect("score")

        question = get_object_or_404(
            Question,
            id=question_ids[question_index],
            category=category,
        )

    return render(
        request,
        "quiz/quiz.html",
        {
            "category": category,
            "question": question,
            "is_last_question": question_index == len(question_ids) - 1,
        },
    )