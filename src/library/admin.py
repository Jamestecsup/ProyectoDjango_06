"""Admin configuration for the library relational models (S04 lab)."""

from django.contrib import admin
from .models import Author, AuthorProfile, Book, Publisher, Category, Publication


class AuthorProfileInline(admin.StackedInline):
    """Inline editor of the OneToOne profile inside the Author change page."""

    model = AuthorProfile
    extra = 0


class BookLineInline(admin.TabularInline):
    """Inline editor of an author's books (one-to-many, the reverse side)."""

    model = Book
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    inlines = [AuthorProfileInline, BookLineInline]


class PublicationInline(admin.TabularInline):
    """Inline editor of the Publication through model with its own data."""

    model = Book.publishers.through
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'pages')
    list_filter = ('author', 'categories', 'publishers')
    search_fields = ('title', 'isbn')
    filter_horizontal = ('categories',)
    inlines = [PublicationInline]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('book', 'publisher', 'publication_date', 'edition')
    list_filter = ('publisher',)
    search_fields = ('book__title', 'publisher__name')