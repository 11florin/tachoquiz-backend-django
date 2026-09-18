from django.contrib import admin
from .models import Category, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ("text_en", "text_ro", "is_correct")
    extra = 4


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_ro", "slug")
    fields = ("name_en", "name_ro", "slug", "image")
    prepopulated_fields = {
        "slug": ("name_en",),
    }


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text_en", "category")

    fieldsets = (
        (
            "Category",
            {
                "fields": ("category",),
            },
        ),
        (
            "English Content",
            {
                "fields": (
                    "text_en",
                    "explanation_en",
                ),
            },
        ),
        (
            "Romanian Content",
            {
                "fields": (
                    "text_ro",
                    "explanation_ro",
                ),
            },
        ),
    )

    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text_en", "question", "is_correct")
    fields = ("question", "text_en", "text_ro", "is_correct")
