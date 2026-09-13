import csv

from django.core.management.base import BaseCommand

from quiz.models import Category, Question, Answer


class Command(BaseCommand):
    help = "Import quiz questions from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="Path to the CSV file containing quiz questions.",
        )

   