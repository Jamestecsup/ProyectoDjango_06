"""Views for the library app (S04 lab).

The catalog is now backed by the relational models Author, Book, Publisher,
Category and Publication:

- book_list: shows every book with its categories, author and publishers.
- book_detail: shows one book and proves the relationships reach the template
  (author, categories, publications/publisher, author profile).
"""

from django.shortcuts import render, get_object_or_404
from .models import Author, Book, Publisher, Category


def book_list(request):
    """List all books, prefetching the related data to avoid N+1 queries."""
    books = Book.objects.select_related('author').prefetch_related(
        'categories', 'publishers', 'publications'
    )
    categories = Category.objects.all()
    context = {
        'books': books,
        'categories': categories,
    }
    return render(request, 'library/book_list.html', context)


def book_detail(request, pk):
    """Show one book with author, categories, publisher(s) and profile."""
    book = get_object_or_404(
        Book.objects.select_related('author', 'author__profile'),
        pk=pk,
    )
    publications = book.publications.select_related('publisher').all()
    context = {
        'book': book,
        'publications': publications,
    }
    return render(request, 'library/book_detail.html', context)


def author_detail(request, pk):
    """Show an author with their books (reverse relation books.all())."""
    author = get_object_or_404(
        Author.objects.select_related('profile').prefetch_related('books'),
        pk=pk,
    )
    return render(request, 'library/author_detail.html', {'author': author})