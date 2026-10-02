"""Movie catalog models for the S05 lab.

Relationships:
- Movie <-> Genre: ManyToManyField, a movie belongs to several genres.
- Rating -> Movie: ForeignKey, each rating belongs to a single movie;
  deleting the movie cascades to its ratings.
- Movie -> Person (director): ForeignKey with SET_NULL so removing a
  person keeps the movie record.
- Movie <-> Person (cast): ManyToManyField for the acting credits.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    """A film genre (Action, Drama, ...)."""

    name = models.CharField(max_length=100, unique=True, verbose_name='name')
    description = models.TextField(blank=True, verbose_name='description')

    class Meta:
        ordering = ['name']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Person(models.Model):
    """A person involved in movies (director or cast member)."""

    name = models.CharField(max_length=120, verbose_name='name')
    birth_date = models.DateField(null=True, blank=True, verbose_name='birth date')
    country = models.CharField(max_length=100, blank=True, verbose_name='country')
    biography = models.TextField(blank=True, verbose_name='biography')

    class Meta:
        ordering = ['name']
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self):
        return self.name


class Movie(models.Model):
    """A movie of the catalog."""

    title = models.CharField(max_length=200, verbose_name='title')
    release_year = models.PositiveIntegerField(db_index=True, verbose_name='release year')
    duration_minutes = models.PositiveIntegerField(default=0, verbose_name='duration (min)')
    synopsis = models.TextField(blank=True, verbose_name='synopsis')
    poster = models.ImageField(upload_to='posters/', blank=True, verbose_name='poster')

    genres = models.ManyToManyField(
        Genre,
        related_name='movies',
        verbose_name='genres',
    )
    director = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='directed_movies',
        verbose_name='director',
    )
    cast = models.ManyToManyField(
        Person,
        blank=True,
        related_name='acted_movies',
        verbose_name='cast',
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        ordering = ['-release_year', 'title']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return f'{self.title} ({self.release_year})'


class Rating(models.Model):
    """A score given to a movie (1-5) with an optional comment."""

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='movie',
    )
    reviewer_name = models.CharField(max_length=120, verbose_name='reviewer')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='score',
    )
    comment = models.TextField(blank=True, verbose_name='comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return f'{self.movie.title} - {self.score}/5 by {self.reviewer_name}'
