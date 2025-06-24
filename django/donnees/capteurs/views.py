from django.shortcuts import render, get_object_or_404, redirect
from .models import Capteur, Donnee
from .forms import CapteurForm
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse, HttpResponse
import csv
from django.utils.dateparse import parse_date

def liste_capteurs(request):
    capteurs = Capteur.objects.all()
    return render(request, 'capteurs/liste_capteurs.html', {'capteurs': capteurs})


def donnees_filtrees(request):
    capteur_id = request.GET.get('capteur_id')
    nom = request.GET.get('nom')
    debut = request.GET.get('debut')
    fin = request.GET.get('fin')

    donnees = Donnee.objects.all().order_by('-timestamp')

    if capteur_id:
        donnees = donnees.filter(capteur__id_capteur=capteur_id)
    if nom:
        donnees = donnees.filter(capteur__nom_capteur__icontains=nom)
    if debut and fin:
        donnees = donnees.filter(timestamp__range=[debut, fin])

    return render(request, 'capteurs/donnees.html', {'donnees': donnees})


def donnees_json(request):
    donnees = Donnee.objects.select_related('capteur').order_by('-timestamp')

    if capteur_id := request.GET.get("capteur_id"):
        donnees = donnees.filter(capteur__id=capteur_id)
    if nom := request.GET.get("nom"):
        donnees = donnees.filter(capteur__nom_capteur__icontains=nom)
    if debut := request.GET.get("debut"):
        donnees = donnees.filter(timestamp__gte=parse_date(debut))
    if fin := request.GET.get("fin"):
        donnees = donnees.filter(timestamp__lte=parse_date(fin))

    data = [
        {
            "timestamp": d.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "capteur": d.capteur.nom_capteur,
            "temperature": d.temperature
        }
        for d in donnees
    ]
    return JsonResponse(data, safe=False)

def donnees_csv(request):
    donnees = Donnee.objects.select_related('capteur').order_by('-timestamp')

    if capteur_id := request.GET.get("capteur_id"):
        donnees = donnees.filter(capteur__id=capteur_id)
    if nom := request.GET.get("nom"):
        donnees = donnees.filter(capteur__nom_capteur__icontains=nom)
    if debut := request.GET.get("debut"):
        donnees = donnees.filter(timestamp__gte=parse_date(debut))
    if fin := request.GET.get("fin"):
        donnees = donnees.filter(timestamp__lte=parse_date(fin))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donnees.csv"'

    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'Capteur', 'Température'])

    for d in donnees:
        writer.writerow([d.timestamp.strftime('%Y-%m-%d %H:%M:%S'), d.capteur.nom_capteur, d.temperature])

    return response


def donnees_graph_json(request):
    donnees = Donnee.objects.all().order_by('-timestamp')
    data_by_capteur = {}

    for d in donnees:
        capteur_id = d.capteur.id
        if capteur_id not in data_by_capteur:
            data_by_capteur[capteur_id] = []
        if len(data_by_capteur[capteur_id]) < 100:
            data_by_capteur[capteur_id].append({
                'timestamp': d.timestamp.isoformat(),
                'temperature': d.temperature,
                'nom': d.capteur.nom_capteur
            })

    return JsonResponse(data_by_capteur)