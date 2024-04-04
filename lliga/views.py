from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django import forms
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.

def index(request):
    return render(request,"index.html")

class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Liga.objects.all())
 
@login_required
def profile(request):
    user = request.user
    return HttpResponse("Profile: " + user.username +
        "<br> Nombre: " + user.first_name + 
        "<br> Email: " + user.last_name
    )

def menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })

def classificacio(request, lliga_id):
    lliga = get_object_or_404(Liga,pk=lliga_id)
    equips = lliga.equipo_set.all()
    classi = []
 
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        for partit in lliga.partido_set.filter(local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partido_set.filter(visitante=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        classi.append( (punts,equip.nombre) )
    # ordenem llista
    classi.sort(reverse=True)
    return render(request,"clasificacion.html",
                {
                    "classificacio":classi,
                    "lliga": lliga
                })

class LigaForm(forms.ModelForm):
    class Meta:
        model = Liga
        fields = ['nombre']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Liga.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("Ya existe una liga con este nombre.")
        return nombre
    
class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre']

class AsignarEquiposForm(forms.ModelForm):
    equipos = forms.ModelMultipleChoiceField(queryset=Equipo.objects.all(), required=False)

    class Meta:
        model = Liga
        fields = ['equipos']


def crear_liga(request):
    if request.method == 'POST':
        form = LigaForm(request.POST)
        if form.is_valid():
            nombre_liga = form.cleaned_data['nombre']
            if Liga.objects.filter(nombre=nombre_liga).exists():
                # Si ya existe una liga con el mismo nombre, muestra un mensaje de error
                return render(request, 'crear_liga.html', {'form': form, 'error_message': 'Ya existe una liga con este nombre'})
            else:
                form.save()
                return redirect('crear_liga')
    else:
        form = LigaForm()
    return render(request, 'crear_liga.html', {'form': form})

def crear_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_equipo')
    else:
        form = EquipoForm()
    return render(request, 'crear_equipo.html', {'form': form})

def asignar_equipos_liga(request):
    if request.method == 'POST':
        equipo_id = request.POST.get('equipo')
        nueva_liga_id = request.POST.get('nueva_liga')

        try:
            equipo = Equipo.objects.get(pk=equipo_id)
            nueva_liga = Liga.objects.get(pk=nueva_liga_id)

            # Cambiar la liga asociada al equipo
            equipo.ligas.add(nueva_liga)

            # Guardar los cambios
            equipo.save()

            return redirect('asignar_equipos_liga_success')
        except (Equipo.DoesNotExist, Liga.DoesNotExist):
            # Manejo de errores si el equipo o la liga no existen
            # Puedes personalizar este manejo según tus necesidades
            return render(request, 'error.html', {'message': 'El equipo o la liga seleccionada no existe.'})
    else:
        ligas = Liga.objects.all()
        equipos = Equipo.objects.all()
        return render(request, 'asignar_equipos_liga.html', {'ligas': ligas, 'equipos': equipos})

def asignar_equipos_liga_success(request):
    return render(request, 'asignar_equipos_liga_success.html')