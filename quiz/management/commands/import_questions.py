import csv

from django.core.management.base import BaseCommand, CommandError
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
        try:
            file = open(csv_file, newline="", encoding="utf-8")
        except FileNotFoundError as error:
            raise CommandError(
                f"CSV file not found: {csv_file}"
            ) from error

        with file:
            reader = csv.DictReader(file)

            required_columns = {
                "category_en",
                "category_ro",
                "question_en",
                "question_ro",
                "explanation_en",
                "explanation_ro",
                "answer_1_en",
                "answer_1_ro",
                "answer_2_en",
                "answer_2_ro",
                "answer_3_en",
                "answer_3_ro",
                "answer_4_en",
                "answer_4_ro",
                "correct_answer",
            }

            missing_columns = required_columns - set(reader.fieldnames or [])

            if missing_columns:
                raise CommandError(
                    "CSV file is missing required columns: "
                    + ", ".join(sorted(missing_columns))
                )

            for row_number, row in enumerate(reader, start=2):
                category_en = row["category_en"].strip()
                category_ro = row["category_ro"].strip()

                question_en = row["question_en"].strip()
                question_ro = row["question_ro"].strip()

                explanation_en = row["explanation_en"].strip()
                explanation_ro = row["explanation_ro"].strip()

                answers = [
                    {
                        "text_en": row["answer_1_en"].strip(),
                        "text_ro": row["answer_1_ro"].strip(),
                    },
                    {
                        "text_en": row["answer_2_en"].strip(),
                        "text_ro": row["answer_2_ro"].strip(),
                    },
                    {
                        "text_en": row["answer_3_en"].strip(),
                        "text_ro": row["answer_3_ro"].strip(),
                    },
                    {
                        "text_en": row["answer_4_en"].strip(),
                        "text_ro": row["answer_4_ro"].strip(),
                    },
                ]

                correct_answer = row["correct_answer"].strip()

                if not category_en or not category_ro:
                    self.stderr.write(
                        f"Row {row_number}: category is required in both languages."
                    )
                    continue

                if not question_en or not question_ro:
                    self.stderr.write(
                        f"Row {row_number}: question is required in both languages."
                    )
                    continue

                if not explanation_en or not explanation_ro:
                    self.stderr.write(
                        f"Row {row_number}: explanation is required in both languages."
                    )
                    continue

                if any(
                    not answer["text_en"] or not answer["text_ro"]
                    for answer in answers
                ):
                    self.stderr.write(
                        f"Row {row_number}: all four answers are required "
                        "in both languages."
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
                        name_en=category_en,
                        defaults={
                            "name_ro": category_ro,
                            "slug": slugify(category_en),
                        },
                    )

                    if not created and category.name_ro != category_ro:
                        category.name_ro = category_ro
                        category.save(update_fields=["name_ro"])

                    if Question.objects.filter(
                        category=category,
                        text_en=question_en,
                    ).exists():
                        self.stdout.write(
                            f"Row {row_number} skipped: "
                            "question already exists."
                        )
                        continue

                    question = Question.objects.create(
                        category=category,
                        text_en=question_en,
                        text_ro=question_ro,
                        explanation_en=explanation_en,
                        explanation_ro=explanation_ro,
                    )

                    for index, answer in enumerate(
                        answers,
                        start=1,
                    ):
                        Answer.objects.create(
                            question=question,
                            text_en=answer["text_en"],
                            text_ro=answer["text_ro"],
                            is_correct=(
                                index == int(correct_answer)
                            ),
                        )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Row {row_number} imported: {question_en}"
                    )
                )
  