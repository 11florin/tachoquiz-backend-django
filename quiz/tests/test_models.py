from django.test import TestCase
from django.utils import translation

from quiz.models import Category


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name_en="Driving Time",
            name_ro="Timp de conducere",
            slug="driving-time",
        )

    def test_category_is_created(self):
        self.assertEqual(self.category.name_en, "Driving Time")
        self.assertEqual(self.category.name_ro, "Timp de conducere")
        self.assertEqual(self.category.slug, "driving-time")

    def test_category_localized_name_in_english(self):
        with translation.override("en"):
            self.assertEqual(
                self.category.localized_name,
                "Driving Time"
            )

    def test_category_localized_name_in_romanian(self):
        with translation.override("ro"):
            self.assertEqual(
                self.category.localized_name,
                "Timp de conducere"
            )