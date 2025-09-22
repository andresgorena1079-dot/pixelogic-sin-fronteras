# cursos/forms.py
from django import forms

from .models import Herramienta, Juego


class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ["nombre", "descripcion", "enlace", "archivo", "imagen"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"placeholder": "Nombre de la herramienta"}
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Describe brevemente la herramienta y para qué sirve.",
                }
            ),
            "enlace": forms.URLInput(attrs={"placeholder": "https://ejemplo.com"}),
        }
        labels = {
            "nombre": "Nombre de la Herramienta",
            "descripcion": "Descripción",
            "enlace": "Enlace de descarga o sitio web",
            "imagen": "Imagen o logo (opcional)",
        }


class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ["nombre", "descripcion", "enlace", "archivo", "imagen"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Nombre del juego"}),
            "descripcion": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Describe brevemente el juego y su objetivo.",
                }
            ),
            "enlace": forms.URLInput(
                attrs={"placeholder": "https://ejemplo.com/jugar"}
            ),
        }
        labels = {
            "nombre": "Nombre del Juego",
            "descripcion": "Descripción",
            "enlace": "Enlace para jugar",
            "imagen": "Imagen o portada (opcional)",
        }
