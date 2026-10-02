"""Admin configuration for the news portal (S06 lab)."""

from django.contrib import admin

from .models import Article, Author, Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'articles_total')
    list_filter = ('articles__categories',)
    search_fields = ('name', 'email')

    @admin.display(description='Articles')
    def articles_total(self, obj):
        return obj.articles.count()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'articles_total')
    list_filter = ('articles__author',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Articles')
    def articles_total(self, obj):
        return obj.articles.count()


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category_list', 'published_at', 'is_published')
    list_filter = ('is_published', 'published_at', 'categories', 'author')
    search_fields = ('title', 'summary', 'body', 'author__name', 'categories__name')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    date_hierarchy = 'published_at'
    list_editable = ('is_published',)

    @admin.display(description='Categories')
    def category_list(self, obj):
        return ', '.join(c.name for c in obj.categories.all())
