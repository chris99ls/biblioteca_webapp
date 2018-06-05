from .models import Libro
from django import forms
import django_filters

class BookFilter(django_filters.FilterSet):

    author = django_filters.CharFilter(lookup_expr='icontains')
    title = django_filters.CharFilter(lookup_expr='icontains')
    isbn = django_filters.NumberFilter(lookup_expr='exact')
    subject = django_filters.ModelMultipleChoiceFilter(queryset=Libro.objects.values_list('subject',flat=True).distinct(),widget=forms.CheckboxSelectMultiple)


    class Meta:
        model = Libro
        fields = ['title','author','subject','isbn']