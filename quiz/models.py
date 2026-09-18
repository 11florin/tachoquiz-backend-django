from django.conf import settings
from django.db import models
from django.utils.translation import get_language

# Create your models here.

class Category(models.Model):
    name_en = models.CharField(max_length=100, verbose_name="Category (English)",)
    name_ro = models.CharField(max_length=100, verbose_name="Category (Romanian)",)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "Categories"

    @property
    def localized_name(self):
        if get_language() == "ro":
            return self.name_ro
        return self.name_en

    def __str__(self):
        return self.name_en


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="questions",)
    text_en = models.TextField(verbose_name="Question (English)")
    text_ro = models.TextField(verbose_name="Question (Romanian)")
    explanation_en = models.TextField(verbose_name="Explanation (English)")
    explanation_ro = models.TextField(verbose_name="Explanation (Romanian)")

    @property
    def localized_text(self):
        if get_language() == "ro":
            return self.text_ro
        return self.text_en


    @property
    def localized_explanation(self):
        if get_language() == "ro":
            return self.explanation_ro
        return self.explanation_en

    def __str__(self):
        return self.text_en


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers",)
    text_en = models.CharField(max_length=255, verbose_name="Answer (English)",)
    text_ro = models.CharField(max_length=255, verbose_name="Answer (Romanian)",)
    is_correct = models.BooleanField(default=False)

    @property
    def localized_text(self):
        if get_language() == "ro":
            return self.text_ro
        return self.text_en

    def __str__(self):
        return self.text_en


class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_results",)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="quiz_results",)
    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-completed_at"]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.category} - "
            f"{self.score}/{self.total_questions}"
        )