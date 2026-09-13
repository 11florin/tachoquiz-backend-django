from django.conf import settings
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="questions",)
    text = models.TextField(verbose_name="Question")
    explanation = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers",)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


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