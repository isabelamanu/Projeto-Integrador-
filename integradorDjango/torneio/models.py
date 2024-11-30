from django.db import models

# Create your models here.

class Torneio(models.Model):
    round = models.JSONField(default=list)
    round2 = models.JSONField(default=list)
    final = models.JSONField(default=list)
    campeao = models.CharField(max_length=60, blank= True)

    def __str__(self) -> str:
        return f"Torneio {self.id}"
