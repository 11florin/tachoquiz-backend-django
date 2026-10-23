from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from quiz.models import Category, RevisionNote


class RevisionNoteCrudTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="notes-user",
            email="notes@example.com",
            password="StrongPass123!",
        )
        self.other_user = get_user_model().objects.create_user(
            username="other-user",
            email="other@example.com",
            password="StrongPass123!",
        )
        self.category = Category.objects.create(
            name_en="Rest periods",
            name_ro="Perioade de odihnă",
            slug="rest-periods",
        )
        self.client.login(username="notes-user", password="StrongPass123!")

    def test_user_can_create_and_view_revision_note(self):
        response = self.client.post(
            reverse("revision-note-create"),
            {
                "title": "Daily rest plan",
                "category": self.category.pk,
                "content": "Break every 4.5 hours and check tachograph logs.",
            },
        )

        note = RevisionNote.objects.get(title="Daily rest plan")
        self.assertRedirects(
            response,
            reverse("revision-note-detail", args=[note.pk]),
        )

        detail_response = self.client.get(
            reverse("revision-note-detail", args=[note.pk])
        )
        self.assertContains(detail_response, "Daily rest plan")

    def test_user_can_edit_their_own_revision_note(self):
        note = RevisionNote.objects.create(
            user=self.user,
            category=self.category,
            title="Original title",
            content="Original content",
        )

        response = self.client.post(
            reverse("revision-note-edit", args=[note.pk]),
            {
                "title": "Updated title",
                "category": self.category.pk,
                "content": "Updated content",
            },
        )

        note.refresh_from_db()
        self.assertRedirects(
            response,
            reverse("revision-note-detail", args=[note.pk]),
        )
        self.assertEqual(note.title, "Updated title")
        self.assertEqual(note.content, "Updated content")

    def test_user_cannot_edit_or_delete_other_users_note(self):
        note = RevisionNote.objects.create(
            user=self.other_user,
            category=self.category,
            title="Private note",
            content="Not for you",
        )

        edit_response = self.client.get(
            reverse("revision-note-edit", args=[note.pk])
        )
        delete_response = self.client.get(
            reverse("revision-note-delete", args=[note.pk])
        )

        self.assertRedirects(edit_response, reverse("revision-notes"))
        self.assertRedirects(delete_response, reverse("revision-notes"))

    def test_user_can_delete_revision_note_with_confirmation(self):
        note = RevisionNote.objects.create(
            user=self.user,
            category=self.category,
            title="Temporary note",
            content="Remove me",
        )

        response = self.client.post(
            reverse("revision-note-delete", args=[note.pk])
        )

        self.assertRedirects(response, reverse("revision-notes"))
        self.assertFalse(RevisionNote.objects.filter(pk=note.pk).exists())
