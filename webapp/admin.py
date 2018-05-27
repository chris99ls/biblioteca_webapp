from django.contrib import admin
from .models import Libro , Sinossi, Prestito
# Register your models here.


admin.site.register(Libro)
admin.site.register(Sinossi)
admin.site.register(Prestito)