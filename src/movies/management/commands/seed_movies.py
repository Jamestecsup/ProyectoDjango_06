"""Seed command for the S05 lab: creates the demo movie catalog.

Usage:
    python manage.py seed_movies

The data includes:
- 4 genres
- 6 persons (directors / cast)
- 10 movies across genres and years
- Ratings in 7 of the 10 movies (requirement: at least 5)
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from movies.models import Genre, Movie, Person, Rating


class Command(BaseCommand):
    help = 'Carga datos de prueba para el laboratorio S05 (catálogo de películas)'

    @transaction.atomic
    def handle(self, *args, **options):
        action, _ = Genre.objects.get_or_create(
            name='Acción', defaults={'description': 'Películas de acción y aventura.'}
        )
        comedy, _ = Genre.objects.get_or_create(
            name='Comedia', defaults={'description': 'Películas de humor.'}
        )
        drama, _ = Genre.objects.get_or_create(
            name='Drama', defaults={'description': 'Historias dramáticas.'}
        )
        scifi, _ = Genre.objects.get_or_create(
            name='Ciencia ficción',
            defaults={'description': 'Futuros, espacio y tecnología.'},
        )

        persons = {}
        for name, country, birth in [
            ('Christopher Nolan', 'Reino Unido', '1970-07-30'),
            ('Denis Villeneuve', 'Canadá', '1967-10-03'),
            ('Greta Gerwig', 'Estados Unidos', '1983-08-04'),
            ('Bong Joon-ho', 'Corea del Sur', '1969-09-14'),
            ('Hayao Miyazaki', 'Japón', '1941-01-05'),
            ('Agnès Varda', 'Francia', '1928-05-30'),
        ]:
            person, _ = Person.objects.get_or_create(
                name=name, defaults={'country': country, 'birth_date': birth}
            )
            persons[name] = person

        catalog = [
            ('El origen', 2010, 148, 'Un ladrón que roba secretos de los sueños.',
             'Christopher Nolan', ['Acción', 'Ciencia ficción']),
            ('Interestelar', 2014, 169, 'Viaje espacial para salvar a la humanidad.',
             'Christopher Nolan', ['Ciencia ficción', 'Drama']),
            ('Dune', 2021, 155, 'La lucha por Arrakis y la especia.',
             'Denis Villeneuve', ['Ciencia ficción', 'Acción']),
            ('Barbie', 2023, 114, 'Barbie descubre el mundo real.',
             'Greta Gerwig', ['Comedia', 'Acción']),
            ('Parásitos', 2019, 132, 'Dos familias de clases opuestas se cruzan.',
             'Bong Joon-ho', ['Drama', 'Comedia']),
            ('El viaje de Chihiro', 2001, 125, 'Una niña en un mundo de espíritus.',
             'Hayao Miyazaki', ['Acción', 'Drama']),
            ('Cleo de 5 a 7', 1962, 90, 'Una cantante espera un diagnóstico.',
             'Agnès Varda', ['Drama']),
            ('El caballero de la noche', 2008, 152, 'Batman enfrenta al Joker.',
             'Christopher Nolan', ['Acción', 'Drama']),
            ('La llegada', 2016, 116, 'Una lingüista contacta extraterrestres.',
             'Denis Villeneuve', ['Ciencia ficción', 'Drama']),
            ('Mujercitas', 2019, 135, 'Las hermanas March crecen y sueñan.',
             'Greta Gerwig', ['Drama', 'Comedia']),
        ]
        genre_map = {
            'Acción': action,
            'Comedia': comedy,
            'Drama': drama,
            'Ciencia ficción': scifi,
        }
        cast_names = list(persons.keys())

        movies = []
        for idx, (title, year, duration, synopsis, director, genre_names) in enumerate(catalog):
            movie, _ = Movie.objects.get_or_create(
                title=title,
                release_year=year,
                defaults={
                    'duration_minutes': duration,
                    'synopsis': synopsis,
                    'director': persons[director],
                },
            )
            if movie.director_id is None:
                movie.director = persons[director]
                movie.save(update_fields=['director'])
            movie.genres.set(genre_map[name] for name in genre_names)
            # Rotate cast so every movie has two credited persons.
            movie.cast.set([persons[cast_names[idx % len(cast_names)]],
                            persons[cast_names[(idx + 2) % len(cast_names)]]])
            movies.append(movie)

        # Ratings in 7 of the 10 movies (lab requires at least 5).
        ratings_plan = {
            'El origen': [('Ana', 5, 'Impecable.'), ('Luis', 4, 'Muy buena.')],
            'Interestelar': [('Ana', 5, 'Emotiva.'), ('María', 5, 'Obra maestra.'),
                             ('Luis', 4, 'Larga pero vale la pena.')],
            'Dune': [('Pedro', 4, 'Visualmente enorme.')],
            'Parásitos': [('Ana', 5, 'Brillante.'), ('María', 5, 'Imprescindible.')],
            'El viaje de Chihiro': [('Luis', 5, 'Magia pura.')],
            'El caballero de la noche': [('Pedro', 5, 'La mejor de Batman.'),
                                         ('Ana', 4, 'Gran ritmo.')],
            'La llegada': [('María', 4, 'Inteligente.')],
            # 'Barbie', 'Cleo de 5 a 7' y 'Mujercitas' quedan sin valoraciones
            # para probar el caso "sin promedio" en la recomendación.
        }
        for movie in movies:
            for reviewer, score, comment in ratings_plan.get(movie.title, []):
                Rating.objects.get_or_create(
                    movie=movie,
                    reviewer_name=reviewer,
                    score=score,
                    defaults={'comment': comment},
                )

        self.stdout.write(self.style.SUCCESS('Datos de películas insertados correctamente.'))
        self.stdout.write(f'Géneros: {Genre.objects.count()}')
        self.stdout.write(f'Personas: {Person.objects.count()}')
        self.stdout.write(f'Películas: {Movie.objects.count()}')
        self.stdout.write(f'Valoraciones: {Rating.objects.count()}')
        rated = Movie.objects.filter(ratings__isnull=False).distinct().count()
        self.stdout.write(f'Películas con valoración: {rated}')
