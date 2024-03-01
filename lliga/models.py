from django.db import models

class Liga(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    ligas = models.ManyToManyField(Liga)
    def __str__(self):
        return self.nombre

class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    nacionalidad = models.CharField(max_length=100)
    edad = models.DateField()
    def __str__(self):
        return self.nombre

class Partido(models.Model):
    class Meta:
        unique_together = ["local","visitante","liga"]
    local = models.ForeignKey(Equipo,on_delete=models.CASCADE,
                    related_name="partits_local")
    visitante = models.ForeignKey(Equipo,on_delete=models.CASCADE,
                    related_name="partits_visitant")
    liga = models.ForeignKey(Liga,on_delete=models.CASCADE)
    detalles = models.TextField(null=True,blank=True)
    inicio = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return "{} - {}".format(self.local,self.visitante)
    def gols_local(self):
        return self.event_set.filter(
            tipo=Event.EventType.GOL,equipo=self.local).count()
    def gols_visitant(self):
        return self.event_set.filter(
            tipo=Event.EventType.GOL,equipo=self.visitante).count()

class Event(models.Model):
    # el tipus d'event l'implementem amb algo tipus "enum"
    class EventType(models.TextChoices):
        GOL = "GOL"
        AUTOGOL = "AUTOGOL"
        FALTA = "FALTA"
        PENALTY = "PENALTY"
        MANOS = "MANOS"
        CESSION = "CESSION"
        FUERA_DE_JUEGO = "FUERA_DE_JUEGO"
        ASISTENCIA = "ASISTENCIA"
        TARGETA_AMARILLA = "TARGETA_AMARILLA"
        TARGETA_ROJA = "TARGETA_ROJA"
    partido = models.ForeignKey(Partido,on_delete=models.CASCADE)
    tiempo = models.TimeField()
    tipo = models.CharField(max_length=30,choices=EventType.choices)
    jugador = models.ForeignKey(Jugador,null=True,
                    on_delete=models.SET_NULL,
                    related_name="events_fets")
    equipo = models.ForeignKey(Equipo,null=True,
                    on_delete=models.SET_NULL)
    # per les faltes
    jugador2 = models.ForeignKey(Jugador,null=True,blank=True,
                    on_delete=models.SET_NULL,
                    related_name="events_rebuts")
    detalles = models.TextField(null=True,blank=True)