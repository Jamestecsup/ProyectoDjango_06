"""Public views for the movies catalog (S05 lab).

The admin panel manages the data; these views prove what requires a
custom view: the public recommendation "same-genre top rated movies".
"""

from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render

from .models import Movie


def _annotated_queryset():
    """Base queryset with rating aggregates to avoid N+1 queries."""
    return (
        Movie.objects.select_related('director')
        .prefetch_related('genres', 'cast', 'ratings')
        .annotate(average_score=Avg('ratings__score'), ratings_total=Count('ratings'))
    )


def movie_list(request):
    """List all movies with their average score."""
    movies = _annotated_queryset().order_by('-release_year', 'title')
    return render(request, 'movies/movie_list.html', {'movies': movies})


def movie_detail(request, pk):
    """Show one movie plus the same-genre top rated recommendations."""
    movie = get_object_or_404(_annotated_queryset(), pk=pk)
    ratings = movie.ratings.all().order_by('-created_at')
    recommendations = (
        _annotated_queryset()
        .filter(genres__in=movie.genres.all())
        .exclude(pk=movie.pk)
        .distinct()
        .order_by('-average_score', '-release_year')[:5]
    )
    return render(
        request,
        'movies/movie_detail.html',
        {
            'movie': movie,
            'ratings': ratings,
            'recommendations': recommendations,
        },
    )
