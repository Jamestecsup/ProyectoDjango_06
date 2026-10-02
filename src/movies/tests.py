"""Tests for the S05 movies lab: admin config, roles and recommendations."""

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from movies.models import Genre, Movie, Person, Rating


class MoviesLabTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_movies', verbosity=0)
        call_command('setup_editors', verbosity=0)

    def test_seed_counts(self):
        self.assertEqual(Genre.objects.count(), 4)
        self.assertEqual(Movie.objects.count(), 10)
        rated = Movie.objects.filter(ratings__isnull=False).distinct().count()
        self.assertGreaterEqual(rated, 5)

    def test_audit_fields_readonly_in_admin(self):
        from movies.admin import MovieAdmin, RatingAdmin
        self.assertIn('created_at', MovieAdmin.readonly_fields)
        self.assertIn('updated_at', MovieAdmin.readonly_fields)
        self.assertIn('created_at', RatingAdmin.readonly_fields)

    def test_rating_inline_registered(self):
        from movies.admin import MovieAdmin, RatingInline
        self.assertIn(RatingInline, MovieAdmin.inlines)

    def test_movie_admin_search_filter(self):
        from movies.admin import MovieAdmin
        self.assertIn('title', MovieAdmin.search_fields[0])
        self.assertTrue(any('name' in field for field in MovieAdmin.search_fields))
        self.assertIn('genres', MovieAdmin.list_filter)
        self.assertIn('release_year', MovieAdmin.list_filter)

    def test_editors_group_permissions(self):
        group = Group.objects.get(name='editores')
        codenames = {p.codename for p in group.permissions.all()}
        self.assertIn('add_movie', codenames)
        self.assertIn('change_movie', codenames)
        self.assertNotIn('delete_movie', codenames)
        editor = User.objects.get(username='editor')
        self.assertTrue(editor.has_perm('movies.add_movie'))
        self.assertTrue(editor.has_perm('movies.change_movie'))
        self.assertFalse(editor.has_perm('movies.delete_movie'))

    def test_recommendation_view(self):
        movie = Movie.objects.filter(genres__isnull=False).first()
        response = self.client.get(reverse('movies:detail', args=[movie.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('recommendations', response.context)
        for rec in response.context['recommendations']:
            self.assertNotEqual(rec.pk, movie.pk)

    def test_movie_list_view(self):
        response = self.client.get(reverse('movies:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['movies']), 10)

    def test_editor_cannot_delete_via_admin(self):
        client = Client()
        self.assertTrue(client.login(username='editor', password='editor12345'))
        movie = Movie.objects.first()
        url = reverse('admin:movies_movie_delete', args=[movie.pk])
        response = client.get(url)
        # Without delete permission the admin must forbid access.
        self.assertIn(response.status_code, (302, 403))
