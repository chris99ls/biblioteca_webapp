from django.contrib import admin
from .models import Libro , Sinossi, Prestito, Gestore, Utenti
# Register your models here.


admin.site.register(Libro)
admin.site.register(Sinossi)
admin.site.register(Prestito)
admin.site.register(Gestore)
admin.site.register(Utenti)