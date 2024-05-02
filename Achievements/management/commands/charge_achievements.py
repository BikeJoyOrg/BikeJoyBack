from django.core.management.base import BaseCommand
from Achievements.models import Achievement, Level
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
class Command(BaseCommand):
    help = 'Carga la información inicial de los Achievements desde un archivo Json.'
    achievements_data = [
        {
            'name': "Aventurero",
            'levels': [
                {'level': 1, 'description': "Viaja un total de 20 km", 'value_required': 20, 'coin_reward': 50, 'xp_reward': 1000},
                {'level': 2, 'description': "Viaja un total de 60 km", 'value_required': 60, 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 3, 'description': "Viaja un total de 150 km", 'value_required': 150, 'coin_reward': 200, 'xp_reward': 1000}
            ]
        },
        {
            'name': "Creador",
            'levels': [
                {'level': 1, 'description': "Crea un total de 10 rutas", 'value_required': 10, 'coin_reward': 50,
                 'xp_reward': 1000},
                {'level': 2, 'description': "Crea un total de 25 rutas", 'value_required': 25, 'coin_reward': 100,
                 'xp_reward': 1000},
                {'level': 3, 'description': "Crea un total de 50 rutas", 'value_required': 50, 'coin_reward': 150,
                 'xp_reward': 1000}
            ]
        },
        {
            'name': "Explorador",
            'levels': [
                {'level': 1, 'description': "Explora un total del 15% del mapa", 'value_required': 15,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 2, 'description': "Explora un total del 50% del mapa", 'value_required': 50,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 3, 'description': "Explora un total del 100% del mapa", 'value_required': 100,
                 'coin_reward': 200, 'xp_reward': 1000}
            ]
        },
        {
            'name': "Entusiasta",
            'levels': [
                {'level': 1, 'description': "Completa un total de 10 rutas", 'value_required': 10,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 2, 'description': "Completa un total de 25 rutas", 'value_required': 25,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 3, 'description': "Completa un total de 50 rutas", 'value_required': 50,
                 'coin_reward': 200, 'xp_reward': 1000}
            ]
        },
        {
            'name': "Apasionado",
            'levels': [
                {'level': 1, 'description': "Visita un total de 10 estaciones", 'value_required': 10,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 2, 'description': "Visita un total de 25 estaciones", 'value_required': 25,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 3, 'description': "Visita un total de 50 estaciones", 'value_required': 50,
                 'coin_reward': 200, 'xp_reward': 1000}
            ]
        },
        {
            'name': "Sociable",
            'levels': [
                {'level': 1, 'description': "Haz 10 amigos", 'value_required': 10,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 2, 'description': "Haz 25 amigos", 'value_required': 25,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 3, 'description': "Haz 50 amigos", 'value_required': 50,
                 'coin_reward': 200, 'xp_reward': 1000}
            ]
        },
        {
            'name': "Crítico",
            'levels': [
                {'level': 1, 'description': "Comenta en 5 rutas que hayas completado", 'value_required': 5,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 2, 'description': "Comenta en 15 rutas que hayas completado", 'value_required': 15,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 3, 'description': "Comenta en 30 rutas que hayas completado", 'value_required': 30,
                 'coin_reward': 200, 'xp_reward': 1000}
            ]
        },
        {
            'name': "Navegante",
            'levels': [
                {'level': 1, 'description': "Completa una navegación 20 veces", 'value_required': 20,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 2, 'description': "Completa una navegación 40 veces", 'value_required': 40,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 3, 'description': "Completa una navegación 70 veces", 'value_required': 70,
                 'coin_reward': 200, 'xp_reward': 1000}
            ]
        },
        {
            'name': "Derrochador",
            'levels': [
                {'level': 1, 'description': "Gasta 100 monedas en la tienda", 'value_required': 100,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 2, 'description': "Gasta 400 monedas en la tienda", 'value_required': 400,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 3, 'description': "Gasta 1000 monedas en la tienda", 'value_required': 1000,
                 'coin_reward': 200, 'xp_reward': 1000}
            ]
        },
        {
            'name': "Criador",
            'levels': [
                {'level': 1, 'description': "Sube 1 mascota a su nivel máximo", 'value_required': 1,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 2, 'description': "Sube 4 mascotas a su nivel máximo", 'value_required': 4,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 3, 'description': "Sube 9 mascotas a su nivel máximo", 'value_required': 9,
                 'coin_reward': 200, 'xp_reward': 1000}
            ]
        },
        {
            'name': "Ecologista",
            'levels': [
                {'level': 1, 'description': "Estalvia un total de 50 de cO2", 'value_required': 50,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 2, 'description': "Estalvia un total de 100 de cO2", 'value_required': 100,
                 'coin_reward': 200, 'xp_reward': 1000},
                {'level': 3, 'description': "Estalvia un total de 200 de cO2", 'value_required': 200,
                 'coin_reward': 200, 'xp_reward': 1000}
            ]
        }
    ]

    def handle(self, *args, **options):
        for achievement_data in self.achievements_data:
            achievement = Achievement.objects.create(name=achievement_data['name'])
            for level_data in achievement_data['levels']:
                Level.objects.create(
                    achievement=achievement,
                    level=level_data['level'],
                    description=level_data['description'],
                    current_value=level_data['current_value'],
                    coin_reward=level_data['coin_reward'],
                    xp_reward=level_data['xp_reward']
                )
        self.stdout.write(self.style.SUCCESS('Información de Achievements cargada correctamente'))