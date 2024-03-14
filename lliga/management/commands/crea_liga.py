from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from random import randint
 
from lliga.models import *
 
faker = Faker(["es_CA","es_ES"])
 
class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'
 
    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)
 
    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Liga.objects.filter(nombre=titol_lliga)
        if lliga.count()>0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return
 
        print("Creem la nova lliga: {}".format(titol_lliga))
        lliga = Liga(nombre=titol_lliga)
        lliga.save()
 
        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0,len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom =  prefix + ciutat
            equip = Equipo(nombre=nom)
            #print(equip)
            equip.save()
            lliga.equipo_set.add(equip)
 
            print("Creem jugadors de l'equip "+nom)
            for j in range(25):
                nom = faker.name()
                fecha_nacimiento = faker.date_of_birth(minimum_age=18, maximum_age=37)
                edad = fecha_nacimiento.strftime('%Y-%m-%d')
                nacionalidad = "Español"
                jugador = Jugador(nombre=nom, equipo=equip, nacionalidad=nacionalidad, edad=edad)
                jugador.save()
                equip.jugador_set.add(jugador)
 
        print("Creem partits de la lliga")
        for local in lliga.equipo_set.all():
            for visitante in lliga.equipo_set.all():
                if local!=visitante:
                    partit = Partido(local=local,visitante=visitante)
                    partit.local = local
                    partit.visitante = visitante
                    partit.liga = lliga
                    partit.save()
                
                    #gols 
                    goles_local = randint(0,7)
                    goles_visitante = randint(0,4)
                    for i in range(0, goles_local):
                        jugador = local.jugador_set.all()[randint(0,24)]
                        gol = Event(
                            tipo = Event.EventType.GOL,
                            jugador = jugador,
                            equipo = local,
                            partido = partit,
                            tiempo = timezone.now()
                        )
                        gol.save()
                        partit.event_set.add(gol)
                    for i in range(0, goles_visitante):
                        jugador = visitante.jugador_set.all()[randint(0,24)]
                        gol = Event(
                            tipo = Event.EventType.GOL,
                            jugador = jugador,
                            equipo = visitante,
                            partido = partit,
                            tiempo = timezone.now()
                        )
                        gol.save()
                        partit.event_set.add(gol)