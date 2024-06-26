from django.db import models

from Users.models import CustomUser


# Create your models here.
class Mascota(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    imgEgg = models.ImageField(upload_to='pets/', null=True, blank=True)
    imgEggl = models.ImageField(upload_to='pets/', null=True, blank=True)
    img1 = models.ImageField(upload_to='pets/', null=True, blank=True)
    img1l = models.ImageField(upload_to='pets/', null=True, blank=True)
    img2 = models.ImageField(upload_to='pets/', null=True, blank=True)
    img2l = models.ImageField(upload_to='pets/', null=True, blank=True)
    img3 = models.ImageField(upload_to='pets/', null=True, blank=True)
    img3l = models.ImageField(upload_to='pets/', null=True, blank=True)
    bonus1 = models.FloatField(default=0)
    bonus2 = models.FloatField(default=0)
    bonus3 = models.FloatField(default=0)

class MascotaAconseguida(models.Model):
    nomMascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    nicknameUsuari = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nivell = models.IntegerField(default=0)
    equipada = models.BooleanField(default=False)

    class Meta:
        unique_together = (('nomMascota', 'nicknameUsuari'),)