from django.core.management.base import BaseCommand
import requests
from django.views.decorators.csrf import csrf_exempt

from Pets.models import Mascota


@csrf_exempt
class Command(BaseCommand):
    help = 'Carga la información inicial de las mascotas de nuestra aplicacion.'

    def handle(self, *args, **options):
        try:
            pet_names = ['Nombre de la mascota 1', 'Nombre de la mascota 2', 'Nombre de la mascota 3',
                         'Nombre de la mascota 4', 'Nombre de la mascota 5', 'Nombre de la mascota 6',
                         'Nombre de la mascota 7', 'Nombre de la mascota 8', 'Nombre de la mascota 9']
            pet_bonus = ['Bonus de la mascota 1', 'Bonus de la mascota 2', 'Bonus de la mascota 3',
                         'Bonus de la mascota 4', 'Bonus de la mascota 5', 'Bonus de la mascota 6',
                         'Bonus de la mascota 7', 'Bonus de la mascota 8', 'Bonus de la mascota 9']
            img_value = 1
            for i in range(9):
                pet = Mascota(
                    name=pet_names[i],
                    img1=img_value,
                    img1l=img_value + 1,
                    img2=img_value + 2,
                    img2l=img_value + 3,
                    img3=img_value + 4,
                    img3l=img_value + 5,
                    bonus=pet_bonus[i]
                )
                pet.save()
                img_value += 6

            self.stdout.write(self.style.SUCCESS('Mascotes creades correctament'))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error al obtener información de mascotas: {e}'))