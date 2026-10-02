"""Public views for the news portal (S06 lab).

The admin panel manages the content; these views only read published
articles and pass them to the template engine (variables, control
tags and filters do the formatting, no business logic in templates).
"""

from django.shortcuts import get_object_or_404, render

from .models import Article, Category


def _published_queryset():
    """Base queryset: only published, newest first, no N+1 queries."""
    return (
        Article.objects.filter(is_published=True)
        .select_related('author')
        .prefetch_related('categories')
        .order_by('-published_at')
    )


def home(request):
    """Front page: list all published articles."""
    articles = _published_queryset()
    categories = Category.objects.order_by('name')
    return render(
        request,
        'news/home.html',
        {'articles': articles, 'categories': categories},
    )


def article_detail(request, slug):
    """Detail of one article with its image, author and categories."""
    article = get_object_or_404(_published_queryset(), slug=slug)
    categories = Category.objects.order_by('name')
    related = (
        _published_queryset()
        .filter(categories__in=article.categories.all())
        .exclude(pk=article.pk)
        .distinct()[:3]
    )
    return render(
        request,
        'news/detail.html',
        {'article': article, 'categories': categories, 'related': related},
    )


def article_by_category(request, slug):
    """List published articles of one category, reusing the card fragment."""
    category = get_object_or_404(Category, slug=slug)
    articles = _published_queryset().filter(categories=category)
    categories = Category.objects.order_by('name')
    return render(
        request,
        'news/category_list.html',
        {'category': category, 'articles': articles, 'categories': categories},
    )
