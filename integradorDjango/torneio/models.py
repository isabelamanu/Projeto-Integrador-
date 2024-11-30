from django.db import models

# Create your models here.

class Torneio(models.Model):
    jogadores = models.JSONField(default=list)
    rounds = models.JSONField(default=list)
    campeao = models.CharField(max_length=60, blank= True)

    def __str__(self) -> str:
        return f"Torneio {self.id}"
