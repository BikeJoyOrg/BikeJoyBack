from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Mascota, MascotaAconseguida

admin.site.register(Mascota)
admin.site.register(MascotaAconseguida)