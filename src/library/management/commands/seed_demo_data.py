"""Seed command for the S04 lab: creates sample data for the library app.

Usage:
    python manage.py seed_demo_data

The data includes:
- 2 Authors with profiles
- 4 Books, at least one in 2 categories
- 3 Categories
- 2 Publishers with a Publication through-record
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from library.models import Author, AuthorProfile, Book, Publisher, Category, Publication


class Command(BaseCommand):
    help = 'Carga datos de prueba para el laboratorio S04 (biblioteca con relaciones)'

    @transaction.atomic
    def handle(self, *args, **options):
        # ----- Authors -----
        a1, _ = Author.objects.get_or_create(name='J. K. Rowling', email='jk@potter.com')
        a1.bio = 'Autora de la saga Harry Potter.'
        a1.save(update_fields=['bio'])

        a2, _ = Author.objects.get_or_create(name='George Orwell', email='orwell@uk.com')
        a2.bio = 'Escritor británico, autor de 1984 y Animal Farm.'
        a2.save(update_fields=['bio'])

        # ----- AuthorProfiles -----
        p1, _ = AuthorProfile.objects.get_or_create(author=a1, defaults={
            'birth_date': '1965-07-31',
            'nationality': 'Británica',
            'website': 'https://jkrowling.com',
        })
        p2, _ = AuthorProfile.objects.get_or_create(author=a2, defaults={
            'birth_date': '1903-06-25',
            'nationality': 'Británica',
            'website': None,
        })

        # ----- Categories -----
        c1, _ = Category.objects.get_or_create(name='Fantasía')
        c2, _ = Category.objects.get_or_create(name='Ciencia ficción')
        c3, _ = Category.objects.get_or_create(name='Clásico')

        # ----- Publishers -----
        pub1, _ = Publisher.objects.get_or_create(name='Scholastic', country='Estados Unidos', founded=1920)
        pub2, _ = Publisher.objects.get_or_create(name='Secker & Warburg', country='Reino Unido', founded=1936)

        # ----- Books -----
        b1, _ = Book.objects.get_or_create(
            title='Harry Potter y la piedra filosofal',
            isbn='978-0747532699',
            author=a1,
            publication_year=1997,
            defaults={'pages': 223, 'summary': 'El primer libro de la saga Harry Potter.'},
        )
        b1.categories.add(c1)
        b1.publishers.add(pub1, through_defaults={'edition': 1, 'publication_date': '1997-06-26'})

        b2, _ = Book.objects.get_or_create(
            title='1984',
            isbn='978-0451524935',
            author=a2,
            publication_year=1949,
            defaults={'pages': 328, 'summary': 'Novela distópica sobre un régimen totalitario.'},
        )
        b2.categories.add(c2)

        b3, _ = Book.objects.get_or_create(
            title='Don Quijote de la Mancha',
            isbn='978-8420461458',
            author=a1,
            publication_year=1605,
            defaults={'pages': 863, 'summary': 'La obra cumbre de la literatura española.'},
        )
        b3.categories.add(c3)

        b4, _ = Book.objects.get_or_create(
            title='Harry Potter y la cámara secreta',
            isbn='978-0747534990',
            author=a1,
            publication_year=1998,
            defaults={'pages': 251, 'summary': 'El segundo libro de la saga Harry Potter.'},
        )
        # Book in two categories
        b4.categories.add(c1, c3)
        b4.publishers.add(pub1, through_defaults={'edition': 2, 'publication_date': '1998-07-08'})

        self.stdout.write(self.style.SUCCESS('Datos de prueba insertados correctamente.'))
        self.stdout.write(f'Autor(a)s: {Author.objects.count()}')
        self.stdout.write(f'Libros: {Book.objects.count()}')
        self.stdout.write(f'Categorías: {Category.objects.count()}')
        self.stdout.write(f'Editoriales: {Publisher.objects.count()}')
        self.stdout.write(f'Publicaciones (through): {Publication.objects.count()}')