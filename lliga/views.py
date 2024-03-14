from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django import forms
from django.shortcuts import redirect

from .models import *

# Create your views here.

def index(request):
    return render(request,"index.html")

class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Liga.objects.all())
 
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

