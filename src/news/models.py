"""News portal models for the S06 lab (template engine).

Relationships:
- Article -> Author: ForeignKey with SET_NULL so deleting an author
  keeps the article (author shown as "Redaccion" fallback).
- Article <-> Category: ManyToManyField, an article belongs to several
  categories and a category groups many articles.
- Featured image: Article.featured_image (ImageField, requires Pillow).
- Publication date: Article.published_at (indexed, orders the front page).
"""

from django.db import models


class Author(models.Model):
    """A news author (editor / journalist)."""

    name = models.CharField(max_length=120, verbose_name='name')
    email = models.EmailField(blank=True, verbose_name='email')
    bio = models.TextField(blank=True, verbose_name='bio')
    photo = models.ImageField(upload_to='authors/', blank=True, verbose_name='photo')

    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name


class Category(models.Model):
    """A news section (Politica, Deportes, Cultura, ...)."""

    name = models.CharField(max_length=100, unique=True, verbose_name='name')
    slug = models.SlugField(max_length=110, unique=True, verbose_name='slug')
    description = models.TextField(blank=True, verbose_name='description')

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Article(models.Model):
    """A news article published in the portal."""

    title = models.CharField(max_length=200, verbose_name='title')
    slug = models.SlugField(max_length=210, unique=True, verbose_name='slug')
    summary = models.TextField(verbose_name='summary')
    body = models.TextField(verbose_name='body')
    featured_image = models.ImageField(
        upload_to='articles/', blank=True, verbose_name='featured image'
    )
    published_at = models.DateTimeField(db_index=True, verbose_name='published at')
    is_published = models.BooleanField(default=True, verbose_name='is published')

    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name='author',
    )
    categories = models.ManyToManyField(
        Category,
        related_name='articles',
        verbose_name='categories',
    )

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title
