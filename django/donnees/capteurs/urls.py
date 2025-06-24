from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_capteurs, name='liste_capteurs'),  
    path('donnees/', views.donnees_filtrees, name='donnees'),  
    path('donnees/json/', views.donnees_json, name='donnees_json'),  
    path('donnees/export/csv/', views.donnees_csv, name='donnees_csv'),
    path('donnees_graph_json/', views.donnees_graph_json, name='donnees_graph_json'),  
]
