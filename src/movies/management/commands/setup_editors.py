"""Setup command for the S05 lab roles: group "editores" + test user.

Usage:
    python manage.py setup_editors

Creates (idempotently):
- Group "editores" with add/change/view on Movie and view-only on
  Genre, Person and Rating (no delete permission anywhere).
- Staff user "editor" (password "editor12345") inside that group,
  so the panel can be checked as editor vs superuser.
"""

from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Crea el grupo editores y el usuario editor del laboratorio S05'

    @transaction.atomic
    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name='editores')

        wanted = [
            ('movies', 'movie', 'add_movie'),
            ('movies', 'movie', 'change_movie'),
            ('movies', 'movie', 'view_movie'),
            ('movies', 'genre', 'view_genre'),
            ('movies', 'person', 'view_person'),
            ('movies', 'rating', 'view_rating'),
        ]
        permissions = Permission.objects.filter(
            content_type__app_label__in={app for app, _, _ in wanted},
            codename__in={codename for _, _, codename in wanted},
        )
        group.permissions.set(permissions)

        user, created = User.objects.get_or_create(
            username='editor',
            defaults={'is_staff': True, 'is_superuser': False},
        )
        user.is_staff = True
        user.is_superuser = False
        user.set_password('editor12345')
        user.save()
        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS('Grupo "editores" configurado.'))
        self.stdout.write(f'Permisos: {sorted(p.codename for p in group.permissions.all())}')
        self.stdout.write(f'Usuario editor: {"creado" if created else "actualizado"} (password: editor12345)')
        self.stdout.write(f'Puede eliminar películas: {user.has_perm("movies.delete_movie")}')
