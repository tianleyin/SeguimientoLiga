from django.contrib import admin

# Register your models here.

from .models import *

class EventInline(admin.TabularInline):
    model = Event
    fields = ["tiempo","tipo","jugador","equipo"]
    ordering = ("tiempo",)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        partido_id = request.resolver_match.kwargs['object_id']
        partido = Partido.objects.get(id=partido_id)
        equips_ids = [partido.local.id, partido.visitante.id]
        qs = Equipo.objects.filter(id__in=equips_ids)

        # Obtener los IDs de los equipos participantes en el partido
        equipo_local_id = partido.local.id
        equipo_visitante_id = partido.visitante.id
        
        # Filtrar los jugadores que pertenecen a los equipos participantes
        jugadores_equipo_local = Jugador.objects.filter(equipo_id=equipo_local_id)
        jugadores_equipo_visitante = Jugador.objects.filter(equipo_id=equipo_visitante_id)
        jugadores_en_partido = jugadores_equipo_local | jugadores_equipo_visitante

        if db_field.name == "equipo":
            kwargs["queryset"] = qs

        if db_field.name == "jugador":
              kwargs["queryset"] = jugadores_en_partido
        return super().formfield_for_foreignkey(db_field, request, **kwargs)      
    
class PartidoAdmin(admin.ModelAdmin):
        # podem fer cerques en els models relacionats
        # (noms dels equips o títol de la lliga)
	search_fields = ["local__nombre","visitante__nombre","liga__nombre"]
        # el camp personalitzat ("resultats" o recompte de gols)
        # el mostrem com a "readonly_field"
	readonly_fields = ["resultado",]
	list_display = ["local","visitante","resultado","liga","inicio"]
	ordering = ("-inicio",)
	inlines = [EventInline,]
	def resultado(self,obj):
		gols_local = obj.event_set.filter(
		                tipo=Event.EventType.GOL,
                                equipo=obj.local).count()
		gols_visit = obj.event_set.filter(
		                tipo=Event.EventType.GOL,
                                equipo=obj.visitante).count()
		return "{} - {}".format(gols_local,gols_visit)

class EquipoInline(admin.TabularInline):
    model = Jugador
    extra = 0

class EquipoAdmin(admin.ModelAdmin):
    inlines = [EquipoInline]


admin.site.register(Liga)
admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Jugador)
admin.site.register(Partido,PartidoAdmin)
admin.site.register(Event)