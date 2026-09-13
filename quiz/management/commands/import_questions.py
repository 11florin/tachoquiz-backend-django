import csv

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from quiz.models import Category, Question, Answer


class Command(BaseCommand):
    help = "Import quiz questions from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="Path to the CSV file containing quiz questions.",
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        self.stdout.write(
            f"Reading CSV file: {csv_file}"
        )

        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row_number, row in enumerate(reader, start=2):
                category_name = row["category"].strip()
                question_text = row["question"].strip()
                explanation = row["explanation"].strip()

                answers = [
                    row["answer_1"].strip(),
                    row["answer_2"].strip(),
                    row["answer_3"].strip(),
                    row["answer_4"].strip(),
                ]

                correct_answer = row["correct_answer"].strip()

                if not category_name:
                    self.stderr.write(
                        f"Row {row_number}: category is required."
                    )
                    continue

                if not question_text:
                    self.stderr.write(
                        f"Row {row_number}: question is required."
                    )
                    continue

                if not explanation:
                    self.stderr.write(
                        f"Row {row_number}: explanation is required."
                    )
                    continue

                if any(not answer for answer in answers):
                    self.stderr.write(
                        f"Row {row_number}: all four answers are required."
                    )
                    continue

                if correct_answer not in {"1", "2", "3", "4"}:
                    self.stderr.write(
                        f"Row {row_number}: "
                        "correct_answer must be between 1 and 4."
                    )
                    continue

                with transaction.atomic():
                    category, created = Category.objects.get_or_create(
                        name=category_name,
                        defaults={
                            "slug": slugify(category_name),
                        },
                    )

                    if Question.objects.filter(
                        category=category,
                        text=question_text,
                    ).exists():
                        self.stdout.write(
                            f"Row {row_number} skipped: "
                            "question already exists."
                        )
                        continue

                    question = Question.objects.create(
                        category=category,
                        text=question_text,
                        explanation=explanation,
                    )

                    for index, answer_text in enumerate(
                        answers,
                        start=1,
                    ):
                        Answer.objects.create(
                            question=question,
                            text=answer_text,
                            is_correct=(
                                index == int(correct_answer)
                            ),
                        )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Row {row_number} imported: {question_text}"
                    )
                )