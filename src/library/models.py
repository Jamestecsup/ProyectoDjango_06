"""Relational models for the S04 lab.

Relationships implemented in this catalog:

- Author <-> Book: ``Book.author`` is a ForeignKey. ``on_delete`` is PROTECT:
  a catalog must not silently destroy books when their author is removed. The
  migration history shows the CASCADE variant (0001) and the change to PROTECT
  (0002), and the README records both behaviors tested in the shell.
- Author <-> AuthorProfile: ``AuthorProfile.author`` is a OneToOneField so the
  biographical data (dates, nationality, photo) lives apart from the main
  record while remaining strictly one profile per author.
- Book <-> Category: ``Book.categories`` is a ManyToManyField; a book belongs
  to several categories and a category groups many books.
- Book <-> Publisher: ``Book.publishers`` is a ManyToManyField through the
  intermediate ``Publication`` model, which stores its own data (publication
  date and edition).
"""

from django.db import models


class Author(models.Model):
    """An author of the catalog."""

    name = models.CharField(max_length=120, verbose_name='name')
    email = models.EmailField(blank=True, verbose_name='email')
    bio = models.TextField(blank=True, verbose_name='bio')

    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name


class AuthorProfile(models.Model):
    """Biographical data separated from the Author main record (OneToOne)."""

    author = models.OneToOneField(
        Author,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='author',
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name='birth date')
    nationality = models.CharField(max_length=100, blank=True, verbose_name='nationality')
    website = models.URLField(blank=True, null=True, verbose_name='website')
    photo = models.ImageField(upload_to='authors/', blank=True, verbose_name='photo')

    class Meta:
        verbose_name = 'Author profile'
        verbose_name_plural = 'Author profiles'

    def __str__(self):
        return f'Profile of {self.author.name}'


class Publisher(models.Model):
    """A publishing house."""

    name = models.CharField(max_length=120, verbose_name='name')
    country = models.CharField(max_length=100, blank=True, verbose_name='country')
    founded = models.PositiveIntegerField(null=True, blank=True, verbose_name='founded year')

    class Meta:
        ordering = ['name']
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return self.name


class Category(models.Model):
    """A thematic category a book can belong to."""

    name = models.CharField(max_length=100, unique=True, verbose_name='name')
    description = models.TextField(blank=True, verbose_name='description')

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Book(models.Model):
    """A book of the catalog."""

    title = models.CharField(max_length=200, verbose_name='title')
    isbn = models.CharField(max_length=13, unique=True, verbose_name='ISBN')
    publication_year = models.PositiveIntegerField(verbose_name='publication year')
    pages = models.PositiveIntegerField(default=0, verbose_name='pages')
    summary = models.TextField(blank=True, verbose_name='summary')
    cover = models.ImageField(upload_to='covers/', blank=True, verbose_name='cover')

    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name='author',
    )
    categories = models.ManyToManyField(
        Category,
        related_name='books',
        verbose_name='categories',
    )
    publishers = models.ManyToManyField(
        Publisher,
        through='Publication',
        related_name='books',
        verbose_name='publishers',
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


class Publication(models.Model):
    """Through model between Book and Publisher, with its own data."""

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name='book',
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name='publisher',
    )
    publication_date = models.DateField(verbose_name='publication date')
    edition = models.PositiveIntegerField(verbose_name='edition')

    class Meta:
        ordering = ['-publication_date']
        unique_together = ('book', 'publisher', 'edition')
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'

    def __str__(self):
        return f'{self.book.title} - {self.publisher.name} (#{self.edition})'