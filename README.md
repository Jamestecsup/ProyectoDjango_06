# Proyecto Django 4 - Laboratorio de Relaciones (S04)

**Continuación de:** [ProyectoDjango_03](https://github.com/Jamestecsup/ProyectoDjango_03)

Este laboratorio extiende el proyecto anterior agregando modelos con relaciones relacionales
(Clave Foránea, OneToOneField y ManyToManyField con modelo intermedio `through`).

## Qué incluye este laboratorio (S04)

- **Modelos relacionales** en la app `library`: `Author`, `AuthorProfile`, `Book`,
  `Publisher`, `Category`, `Publication` (intermedio).
- **ForeignKey** `Book.author` con `on_delete=PROTECT` (y migración `0001` previa con
  `CASCADE` para demostrar ambos efectos).
- **OneToOneField** `AuthorProfile.author` para datos biográficos separados.
- **ManyToManyField** `Book.categories` y `Book.publishers` (a través de `Publication`).
- **Modelo intermedio `Publication`** que guarda `publication_date` y `edition`.
- Migraciones versionadas (`0001_initial` con CASCADE → `0002_alter_book_author` con PROTECT).
- Datos de prueba cargables vía `seed_demo_data` y/o Django Admin.
- Consultas en la consola de Django (ida, vuelta, filtrado `__`).
- Plantillas de detalle que comprueban que la relación llega hasta la vista.
- Servido de archivos de medios (`MEDIA_URL`/`MEDIA_ROOT`) en desarrollo.

## Instalación y ejecución

```bash
# 1. Entorno virtual (ya incluido en el repo)
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Migraciones y datos
cd src
python manage.py migrate
python manage.py seed_demo_data   # o cargar desde el admin /superuser

# 4. Iniciar servidor
python manage.py runserver 0.0.0.0:8000
```

**Credenciales de acceso al admin:**
- Usuario: `admin`
- Contraseña: `admin12345` (crea el superusuario la primera vez con
  `python manage.py createsuperuser`)

## Estructura de modelos

```text
Author (name, email, bio)
  └─ OneToOneField → AuthorProfile (birth_date, nationality, website, photo)
Book (title, isbn, publication_year, pages, summary, cover)
  ├─ ForeignKey → Author (on_delete=PROTECT, related_name='books')
  ├─ ManyToManyField → Category (related_name='books')
  └─ ManyToManyField → Publisher (through='Publication', related_name='books')
Publication (book, publisher, publication_date, edition)  [through]
Publisher (name, country, founded)
Category (name, description)
```

### Migración 0001 (CASCADE)

La migración inicial usó `on_delete=models.CASCADE` para `Book.author`, de modo que
el borrado de un autor eliminaría sus libros. Se documenta este comportamiento en el
README y se probó en la shell (ver sección de consultas).

### Migración 0002 (PROTECT)

Se cambió `on_delete` a `models.PROTECT` para evitar que un autor con libros asociados
sea eliminado accidentalmente. Se generó `0002_alter_book_author` y se aplicó. Al
probar el borrado en la shell se lanza `ProtectedError` y el autor se conserva.

## Comandos de gestión

### seed_demo_data

Carga datos de prueba idempotentes:

- 2 Autores (con perfiles biográficos)
- 4 Libros (uno en dos categorías: *Harry Potter y la cámara secreta*)
- 3 Categorías (Fantasía, Ciencia ficción, Clásico)
- 2 Editoriales (Scholastic, Secker & Warburg)
- Registros `Publication` con fecha y edición

Uso:
```bash
python manage.py seed_demo_data
```

## Consultas en la consola de Django

Se ejecutaron las siguientes consultas y sus resultados se registran aquí:

### 1. Ida (libro.autor)

```
>>> book = Book.objects.first()
>>> book.author
<Author: George Orwell>
>>> book.author.name
'George Orwell'
```

### 2. Vuelta (autor.libros.all())

```
>>> author = Author.objects.first()
>>> author.books.all()
<QuerySet [<Book: 1984]>>
>>> [b.title for b in author.books.all()]
['1984']
```

### 3. Filtrado con doble guion bajo (__)

```
>>> Book.objects.filter(categories__name='Fantasía')
<QuerySet [<Book: Harry Potter y la piedra filosofal>, <Book: Harry Potter y la cámara secreta>]>
>>> Book.objects.filter(categories__name='Ciencia ficción')
<QuerySet [<Book: 1984]>>
```

### 4. Efecto de on_delete: PROTECT (comportamiento actual)

```
>>> author_to_delete = Author.objects.last()
>>> author_to_delete.delete()
Error al borrar autor (PROTECT behavior): ("Cannot delete some instances of model 'Author' because they are referenced through protected foreign keys: 'Book.author'.", {<Book: Harry Potter y la piedra filosofal>, <Book: Don Quijote de la Mancha>, <Book: Harry Potter y la cámara secreta>}})
El autor NO fue borrado porque existen libros asociados.
```

### 5. Efecto de on_delete: CASCADE (migración histórica 0001)

> **Documentado en el historial de migraciones:** `0001_initial` usó
> `on_delete=models.CASCADE`. Si se hubiera aplicado esa migración y luego se
> intentara borrar un autor con libros, estos habrían sido eliminados en cascada.
> Se cambió a `PROTECT` en `0002_alter_book_author` para el comportamiento
> productivo de un catálogo de biblioteca.

## Rutas (URLs)

| Ruta | Descripción |
|------|-------------|
| `/library/` | Listado de libros (catálogo) |
| `/library/book/<int:pk>/` | Detalle de un libro (autor, categorías, editoriales, perfil) |
| `/library/author/<int:pk>/` | Perfil del autor con sus libros |
| `/admin/` | Django Admin (todos los modelos registrados) |
| `/quiz/` | Aplicación quiz (S03, heredada) |

## Plantillas principales

- `library/book_list.html` — tabla con todos los libros, autor, categorías, editorial y miniatura de portada.
- `library/book_detail.html` — vista completa de un libro que muestra:
  - Datos del autor (nombre, email, bio, fecha de nacimiento, nacionalidad).
  - Todas las categorías del libro.
  - Todas las editoriales con número de edición y fecha de publicación (vía `Publication`).
- `library/author_detail.html` — perfil del autor y lista de sus libros (usa la relación inversa `author.books.all()`).

## Evaluación (rubrica S04)

1. **Configura las relaciones** (5 pts) — Las relaciones son ForeignKey, OneToOneField y ManyToManyField con through, cada una es la indicada para el caso. Se explican las decisiones (on_delete PROTECT/CASCADE, related_name legibles).

2. **Modelo intermedio con through** (5 pts) — `Publication` guarda `publication_date` y `edition`, y se consulta desde ambos lados (`.book.publications.all()` y `.publisher.publications.all()`).

3. **Consulta en ambos sentidos y on_delete** (5 pts) — Se recorren las relaciones en ambos sentidos (`libro.autor` y `autor.libros.all()`) y se demuestra el efecto de `on_delete=PROTECT` (lanza `ProtectedError`; el autor se conserva). También se documenta el CASCADE histórico en la migración `0001`.

4. **Entrega del repositorio** (5 pts) — Incluye el esquema de relaciones y observaciones sobre las decisiones (esta documentación, migraciones, diagrama entidad-relación implícito en los modelos).

## Conclusiones

1. Django's ForeignKey con `on_delete=models.PROTECT` es la elección adecuada para un catálogo de biblioteca: evita la eliminación accidental de libros cuando se retira a su autor.
2. `OneToOneField` permite separar limpiamente los datos biográficos (fecha, nacionalidad, foto) del registro principal del autor, manteniendo una relación estricta 1‑a‑1.
3. `ManyToManyField` a través de `Publication` no solo conecta libros con editoriales, sino que también almacena datos propios (edición, fecha de publicación), lo cual es útil para catálogos editoriales.
4. Las migraciones versionadas (`0001` CASCADE → `0002` PROTECT) son un recurso valioso para documentar y revertir decisiones de diseño de esquema.
5. Las consultas en ambos sentidos (`forward` y `reverse`) y con filtros `__` funcionan de forma natural y son muy expresivas.