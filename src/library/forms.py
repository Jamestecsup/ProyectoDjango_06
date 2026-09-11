from django import forms

GENEROS = [
    ('Novela', 'Novela'),
    ('Ciencia ficción', 'Ciencia ficción'),
    ('Infantil', 'Infantil'),
    ('Clásico', 'Clásico'),
    ('Fantasía', 'Fantasía'),
    ('Otro', 'Otro'),
]


class LibroForm(forms.Form):
    """Formulario para registrar un nuevo libro en el catálogo.

    Usa forms.Form (no ModelForm) porque no existe un modelo de base de datos:
    los datos se agregan a la lista estática definida en models.py.
    """
    titulo = forms.CharField(
        max_length=120,
        label='Título',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre del libro'}),
    )
    autor = forms.CharField(
        max_length=120,
        label='Autor',
        widget=forms.TextInput(attrs={'placeholder': 'Autor de la obra'}),
    )
    genero = forms.ChoiceField(
        choices=GENEROS,
        label='Género',
    )
    anio_publicacion = forms.IntegerField(
        label='Año de publicación',
        min_value=0,
        max_value=2100,
        widget=forms.NumberInput(attrs={'placeholder': 'Ej: 1998'}),
    )
    disponible = forms.BooleanField(
        label='Disponible para préstamo',
        required=False,
        initial=True,
    )
