from .models import Libro
from django import forms
import django_filters

class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Libro
        fields = {
            'title': ['icontains', ],
            'author': ['icontains', ],
            'subject': ['icontains', ],
            'isbn': ['exact',  ],
        }