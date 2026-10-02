"""Tests for the S06 news portal (template engine)."""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, Author, Category


class NewsPortalTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Politica', slug='politica')
        self.article = Article.objects.create(
            title='Test article with a long summary ' * 5,
            slug='test-article',
            summary='Summary word ' * 60,
            body='Body with <b>html tag</b> inside.',
            published_at=timezone.now(),
            author=self.author,
            is_published=True,
        )
        self.article.categories.add(self.category)

    def test_home_uses_inheritance_and_fragment(self):
        response = self.client.get(reverse('news:home'))
        self.assertEqual(response.status_code, 200)
        # base.html block title
        self.assertContains(response, 'Portada - Portal de noticias')
        # card fragment reused
        self.assertContains(response, 'class="card"')
        # url tag links (no hardcoded addresses)
        self.assertContains(response, f"/news/article/{self.article.slug}/")
        self.assertContains(response, f"/news/category/{self.category.slug}/")

    def test_home_empty_case(self):
        Article.objects.all().delete()
        response = self.client.get(reverse('news:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No hay noticias publicadas todavia.')

    def test_home_applies_date_and_truncate_filters(self):
        response = self.client.get(reverse('news:home'))
        # truncatewords:30 adds ellipsis character
        self.assertContains(response, '…')
        # date filter output is present (day number of published_at)
        self.assertContains(response, self.article.published_at.strftime('%Y'))

    def test_detail_shows_image_author_categories(self):
        response = self.client.get(reverse('news:detail', args=[self.article.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test article')
        self.assertContains(response, 'Test Author')
        self.assertContains(response, 'Politica')

    def test_category_list_reuses_card_fragment(self):
        response = self.client.get(reverse('news:by_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Seccion: Politica')
        self.assertContains(response, 'class="card"')

    def test_static_css_is_used(self):
        response = self.client.get(reverse('news:home'))
        self.assertContains(response, 'css/style.css')

    def test_autoescape_shows_html_as_text(self):
        response = self.client.get(reverse('news:detail', args=[self.article.slug]))
        # Django autoescape: the tag is escaped, not rendered as HTML.
        self.assertContains(response, '&lt;b&gt;html tag&lt;/b&gt;')
        self.assertNotContains(response, '<b>html tag</b>')

    def test_unpublished_not_in_portal(self):
        self.article.is_published = False
        self.article.save()
        response = self.client.get(reverse('news:home'))
        self.assertNotContains(response, 'Test article')
