from django.db import models

class Capteur(models.Model):
    id_capteur = models.CharField(max_length=20, primary_key=True)
    nom_capteur = models.CharField(max_length=50)
    lieu = models.CharField(max_length=50)
    emplacement = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'capteur'

class Donnee(models.Model):
    id = models.AutoField(primary_key=True)
    capteur = models.ForeignKey(Capteur, to_field='id_capteur', db_column='capteur_id', on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'donnee'

