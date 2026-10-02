"""Admin configuration for the movies catalog (S05 lab)."""

from django.contrib import admin
from django.db.models import Avg, Count

from .models import Genre, Movie, Person, Rating


class RatingInline(admin.TabularInline):
    """Inline editor of ratings inside the movie change page."""

    model = Rating
    extra = 1
    fields = ('reviewer_name', 'score', 'comment', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'release_year',
        'director',
        'genre_list',
        'average_score',
        'ratings_total',
    )
    list_filter = ('release_year', 'genres', 'director')
    search_fields = ('title', 'director__name', 'cast__name', 'genres__name')
    filter_horizontal = ('genres', 'cast')
    inlines = [RatingInline]
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Genres')
    def genre_list(self, obj):
        return ', '.join(g.name for g in obj.genres.all())

    @admin.display(description='Avg. score')
    def average_score(self, obj):
        ratings = obj.ratings.all()
        if not ratings:
            return '-'
        total = sum(r.score for r in ratings)
        return f'{total / len(ratings):.1f}'

    @admin.display(description='Ratings')
    def ratings_total(self, obj):
        return obj.ratings.count()


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'movies_total')
    search_fields = ('name',)

    @admin.display(description='Movies')
    def movies_total(self, obj):
        return obj.movies.count()


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'birth_date', 'directed_total')
    list_filter = ('country',)
    search_fields = ('name', 'country')

    @admin.display(description='Directed')
    def directed_total(self, obj):
        return obj.directed_movies.count()


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'reviewer_name', 'score', 'created_at')
    list_filter = ('score', 'movie')
    search_fields = ('movie__title', 'reviewer_name')
    readonly_fields = ('created_at',)
