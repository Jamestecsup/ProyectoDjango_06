"""Seed command for the S06 lab: creates the demo news portal content.

Usage:
    python manage.py seed_news

Creates (idempotent):
- 3 categories: Politica, Deportes, Cultura
- 3 authors
- 6 articles (2 per category, one shared between two categories)
- The "escape" article body contains a literal HTML tag to prove
  Django autoescape in the detail template.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from news.models import Article, Author, Category


class Command(BaseCommand):
    help = 'Carga datos de prueba para el laboratorio S06 (portal de noticias)'

    @transaction.atomic
    def handle(self, *args, **options):
        politics, _ = Category.objects.get_or_create(
            slug='politica',
            defaults={
                'name': 'Politica',
                'description': 'Actualidad politica nacional e internacional.',
            },
        )
        sports, _ = Category.objects.get_or_create(
            slug='deportes',
            defaults={
                'name': 'Deportes',
                'description': 'Resultados, fichajes y cronicas deportivas.',
            },
        )
        culture, _ = Category.objects.get_or_create(
            slug='cultura',
            defaults={
                'name': 'Cultura',
                'description': 'Libros, cine, musica y agenda cultural.',
            },
        )

        ana, _ = Author.objects.get_or_create(
            name='Ana Torres',
            defaults={'email': 'ana@example.com', 'bio': 'Editora de politica.'},
        )
        luis, _ = Author.objects.get_or_create(
            name='Luis Quispe',
            defaults={'email': 'luis@example.com', 'bio': 'Cronista deportivo.'},
        )
        maria, _ = Author.objects.get_or_create(
            name='Maria Flores',
            defaults={'email': 'maria@example.com', 'bio': 'Periodista cultural.'},
        )

        now = timezone.now()
        catalog = [
            (
                'Congreso aprueba nueva ley de transparencia',
                'congreso-aprueba-ley-transparencia',
                'El pleno aprobo por mayoria la norma que obliga a publicar '
                'contratos y agendas en formato abierto en todas las entidades.',
                'El pleno del Congreso aprobo esta semana la nueva ley de '
                'transparencia con 78 votos a favor. La norma obliga a publicar '
                'contratos, agendas y declaraciones en datos abiertos.\n\n'
                'La sociedad civil saludo la medida y pidio plazos claros.',
                now.replace(hour=8, minute=0),
                ana,
                [politics],
            ),
            (
                'Elecciones regionales: lo que debes saber',
                'elecciones-regionales-guia',
                'Fechas, candidatos y reglas de la jornada electoral regional '
                'explicadas de forma breve para ir a votar informado.',
                'Este es un <strong>texto con etiqueta HTML</strong> guardado '
                'tal cual en el cuerpo para probar el escapado automatico.\n\n'
                'Si el motor funciona, la pagina muestra la etiqueta como texto '
                'visible y no como negrita, porque Django escapa por defecto.',
                now.replace(hour=9, minute=30),
                ana,
                [politics, culture],
            ),
            (
                'Seleccion nacional clasifica a la final',
                'seleccion-clasifica-final',
                'Con un gol en el ultimo minuto, la seleccion sello su pase a '
                'la final ante un estadio lleno y una gran actuacion colectiva.',
                'La seleccion nacional vencio 2-1 con un gol en el minuto 93. '
                'El tecnico destaco el orden tactico y el apoyo de la hinchada.\n\n'
                'La final se jugara el domingo en el estadio nacional.',
                now.replace(hour=10, minute=15),
                luis,
                [sports],
            ),
            (
                'Fichaje estrella revoluciona el torneo local',
                'fichaje-estrella-torneo-local',
                'El club lider anuncio un fichaje internacional que promete '
                'cambiar la pelea por el titulo en la segunda mitad del torneo.',
                'El club lider confirmo el fichaje por dos temporadas. El jugador '
                'llega con un promedio de 20 goles por campana.\n\n'
                'Los abonados podran ver la presentacion el viernes.',
                now.replace(hour=11, minute=0),
                luis,
                [sports],
            ),
            (
                'Festival de cine anuncia su programacion',
                'festival-cine-programacion',
                'Mas de 60 peliculas, homenajes y talleres gratuitos forman '
                'parte de la edicion de este ano del festival de cine.',
                'El festival proyectara mas de 60 titulos en cinco sedes. Habra '
                'homenaje a directoras pioneras y talleres gratuitos.\n\n'
                'La inauguracion sera al aire libre con ingreso libre.',
                now.replace(hour=12, minute=0),
                maria,
                [culture],
            ),
            (
                'Biblioteca municipal reabre con 10 mil libros',
                'biblioteca-reabre-diez-mil-libros',
                'Tras meses de remodelacion, la biblioteca reabre con sala '
                'infantil, mediateca y una coleccion ampliada de autores locales.',
                'La biblioteca reabre con 10 mil libros catalogados, sala '
                'infantil y mediateca. El horario sera de lunes a sabado.\n\n'
                'Vecinos y escolares ya pueden tramitar su carnet gratuito.',
                now.replace(hour=13, minute=30),
                maria,
                [culture],
            ),
        ]

        for title, slug, summary, body, published_at, author, cats in catalog:
            article, created = Article.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'summary': summary,
                    'body': body,
                    'published_at': published_at,
                    'author': author,
                    'is_published': True,
                },
            )
            if not created:
                article.title = title
                article.summary = summary
                article.body = body
                article.published_at = published_at
                article.author = author
                article.is_published = True
                article.save()
            article.categories.set(cats)

        self.stdout.write(self.style.SUCCESS('Datos de noticias insertados correctamente.'))
        self.stdout.write(f'Categorias: {Category.objects.count()}')
        self.stdout.write(f'Autores: {Author.objects.count()}')
        self.stdout.write(f'Articulos: {Article.objects.count()}')
