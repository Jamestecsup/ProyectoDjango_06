"""config URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('library/', include('library.urls')),
    path('movies/', include('movies.urls')),
    path('news/', include('news.urls')),
    path('quiz/', include('quiz.urls')),
]

# Serve uploaded media and project static files during development only.
# (Static files are also served automatically by runserver with DEBUG;
# the explicit route below lets the test client resolve /static/ too.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
