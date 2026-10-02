# Proyecto Django 5 - Laboratorio de Administración (S05)

**Continuación de:** [ProyectoDjango_04](https://github.com/Jamestecsup/ProyectoDjango_04)

Este laboratorio continúa el proyecto anterior (S04: biblioteca con relaciones, apps `library`,
`quiz` y `core`) agregando la app `movies`: un catálogo de películas gestionado desde el
administrador de Django (`ModelAdmin` con listado/filtros/búsqueda, valoraciones en línea,
auditoría de solo lectura y grupos con permisos), más una vista pública de recomendación
(películas del mismo género mejor valoradas). El detalle del S05 está en la sección
[Detalle del laboratorio S05](#detalle-del-laboratorio-s05); las secciones S04 se conservan
como antecedente heredado del repo 4.

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

## Conclusiones (S04)

1. Django's ForeignKey con `on_delete=models.PROTECT` es la elección adecuada para un catálogo de biblioteca: evita la eliminación accidental de libros cuando se retira a su autor.
2. `OneToOneField` permite separar limpiamente los datos biográficos (fecha, nacionalidad, foto) del registro principal del autor, manteniendo una relación estricta 1‑a‑1.
3. `ManyToManyField` a través de `Publication` no solo conecta libros con editoriales, sino que también almacena datos propios (edición, fecha de publicación), lo cual es útil para catálogos editoriales.
4. Las migraciones versionadas (`0001` CASCADE → `0002` PROTECT) son un recurso valioso para documentar y revertir decisiones de diseño de esquema.
5. Las consultas en ambos sentidos (`forward` y `reverse`) y con filtros `__` funcionan de forma natural y son muy expresivas.

---

## Detalle del laboratorio S05

**Continuación acumulativa de S04.** Se conserva `library`, `quiz` y `core`, y se
agrega la aplicación `movies` para el caso del laboratorio: catálogo de películas
gestionado desde el panel de Django.

### Qué incluye este laboratorio (S05)

- **App `movies`** declarada en `INSTALLED_APPS` (`src/config/settings.py`).
- **Modelos** `Genre`, `Person`, `Movie` y `Rating` con sus campos, `Meta` y
  `__str__` (`src/movies/models.py`):
  - `Movie.genres` es `ManyToManyField` a `Genre`.
  - `Rating.movie` es `ForeignKey` a `Movie` con `CASCADE` (al borrar la película
    se borran sus valoraciones).
  - `Movie.director` es `ForeignKey` a `Person` con `SET_NULL` y `Movie.cast` es
    `ManyToManyField` a `Person` (reparto).
  - `Movie.poster` es `ImageField` (requiere Pillow, ya en `requirements.txt`).
  - Auditoría: `Movie.created_at` (`auto_now_add`), `Movie.updated_at`
    (`auto_now`) y `Rating.created_at` (`auto_now_add`).
- **Migración versionada** `movies/0001_initial.py` (generada con
  `makemigrations`, aplicada con `migrate`).
- **Admin personalizado** (`src/movies/admin.py`):
  - Los cuatro modelos registrados; `Rating` además como `RatingInline`
    (`TabularInline`) dentro del formulario de `Movie`.
  - `MovieAdmin.list_display = title, release_year, director, genre_list, average_score, ratings_total`.
  - `MovieAdmin.list_filter = release_year, genres, director` (género y año).
  - `MovieAdmin.search_fields = title, director__name, cast__name, genres__name`
    (título y nombre).
  - `readonly_fields = created_at, updated_at` (y `created_at` en `Rating`): el
    panel ya no permite editar la auditoría.
- **Datos de prueba**: `python manage.py seed_movies` crea 4 géneros, 6 personas,
  10 películas y 12 valoraciones en 7 de las 10 películas (el mínimo pedido era 5).
- **Roles y permisos**: `python manage.py setup_editors` crea el grupo `editores`
  y el usuario `editor` (ver tabla de roles).
- **Vista pública de recomendación** "películas del mismo género mejor valoradas"
  (`src/movies/views.py`, plantillas `movies/movie_list.html` y
  `movies/movie_detail.html`): lo que el panel no hace solo (promedios,
  orden por valoración, recomendaciones cruzadas) exige una vista propia.
- **Tests**: `src/movies/tests.py` (8 pruebas: conteos, `readonly`, inline,
  filtros/búsqueda, permisos del grupo, recomendación y veto de borrado).

### Instalación y ejecución

```bash
pip install -r requirements.txt

cd src
python manage.py migrate
python manage.py seed_movies      # 4 géneros, 6 personas, 10 películas, 12 valoraciones
python manage.py setup_editors    # grupo editores + usuario editor/editor12345

# Superusuario (si la BD es nueva)
python manage.py createsuperuser  # sugerido: admin / admin12345

python manage.py test movies
python manage.py runserver 0.0.0.0:8000
```

**Credenciales de acceso al admin (`/admin/`):**

| Usuario  | Contraseña   | Rol / grupo | Permisos en `movies` |
|----------|--------------|-------------|----------------------|
| `admin`  | `admin12345` | superusuario | Todo (añadir, cambiar, eliminar, ver). |
| `editor` | `editor12345` | `editores` | `add_movie`, `change_movie`, `view_movie`, `view_genre`, `view_person`, `view_rating`. Sin ningún `delete_*` ni `add/change` sobre géneros, personas o valoraciones. |

### Estructura de modelos (`movies`)

```text
Genre (name unique, description)
Person (name, birth_date, country, biography)
Movie (title, release_year, duration_minutes, synopsis, poster,
       created_at, updated_at)
  ├─ ManyToManyField → Genre (related_name='movies')
  ├─ ForeignKey → Person director (SET_NULL, related_name='directed_movies')
  └─ ManyToManyField → Person cast (blank, related_name='acted_movies')
Rating (movie FK CASCADE, reviewer_name, score 1-5, comment, created_at)
```

### Cómo se reparten los roles y por qué

| Rol | Pertenece a | Ve en el panel | Puede hacer | No puede hacer |
|-----|-------------|----------------|-------------|----------------|
| Superusuario `admin` | — (todo) | Los 4 modelos + resto del proyecto | Crear, editar y eliminar todo; gestionar usuarios/grupos | Nada vetado (uso solo para configurar). |
| Editor `editor` | Grupo `editores` | Películas (lista, alta, edición), más lectura de géneros, personas y valoraciones para rellenar el formulario | `add_movie`, `change_movie` (cargar el catálogo del día a día) | Eliminar películas (`delete_movie` denegado: desaparece la acción `delete_selected` y el botón Eliminar, comprobado con `editor` logueado; devuelve 302/403), crear géneros/personas o dar permisos. |

**Por qué así:** el borrado es la operación destructiva (rompería promedios,
recomendaciones y el `CASCADE` de valoraciones), por eso queda reservada al
administrador; el editor necesita `view_*` sobre los modelos relacionados porque
el formulario de película los usa (selector de géneros, director y reparto), pero
no debe inventar géneros ni tocar usuarios. Así cada uno ve solo lo que le toca.

### Rutas (URLs)

| Ruta | Descripción |
|------|-------------|
| `/movies/` | Listado público de películas con promedio y nº de valoraciones. |
| `/movies/<int:pk>/` | Detalle + valoraciones + recomendadas del mismo género mejor valoradas. |
| `/admin/` | Panel: los 4 modelos de `movies` (película con valoraciones en línea). |
| `/library/`, `/quiz/`, `/` | Apps heredadas de S04/S03 (acumulativo). |

### Comparación para el entregable (qué capturar)

- **Panel antes vs después:** registro simple (`admin.site.register`) muestra solo
  el `__str__`; tras `ModelAdmin` el listado de películas muestra columnas útiles
  (título, año, director, géneros, promedio, nº valoraciones), filtros por género
  y año, y búsqueda por título/nombre; el formulario trae las valoraciones en
  línea y la auditoría como solo lectura.
- **Superusuario vs editor:** con `admin` se ven Eliminar, Guardar, usuarios y
  grupos; con `editor` desaparecen la acción de borrado, el botón Eliminar y la
  gestión de usuarios/grupos (solo lectura de catálogos auxiliares).

### Evaluación (rúbrica S05)

1. **Configura el administrador para modelos relacionados (5):** 4 modelos
   registrados y editables + `RatingInline` dentro de `Movie`.
2. **Personaliza listado, filtros y búsqueda (5):** `list_display` útil,
   `list_filter` por género/año, `search_fields` por título/nombre (verificado 200
   en búsqueda y filtros).
3. **Administra el acceso (5):** grupo `editores` + usuario `editor` comprobado
   (puede añadir/cambiar, no puede eliminar: sin `delete_selected`, 302/403).
4. **Entrega del repositorio con observaciones (5):** esta documentación + tabla de
   roles y su justificación + tests (`test movies`: 8 OK).

### Conclusiones (S05)

1. El panel da las cuatro operaciones sin escribir vistas, pero la personalización
   (`list_display`, `list_filter`, `search_fields`, inlines, `readonly_fields`) es
   lo que lo vuelve usable para el caso real.
2. Los inlines (`Rating` dentro de `Movie`) evitan salir del registro padre y
   mantienen la coherencia del `ForeignKey`.
3. Los campos de auditoría deben ser `readonly_fields`: informan sin dejar que el
   operador reescriba la historia.
4. Los permisos por grupo separan el trabajo destructivo (borrar, solo admin) del
   trabajo diario (alta/edición, editores), y se comprueban entrando como editor.
5. Lo que el panel no resuelve (promedios, ranking por género, recomendaciones)
   exige una vista propia: el panel administra, la vista pública recomienda.