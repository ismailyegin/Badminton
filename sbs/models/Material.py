from django.db import models
from sbs.models.Document import Document
from sbs.models.Penal import Penal


class Meterial(models.Model):
    ayakkabi = models.CharField(max_length=120, blank=True, null=True)
    esofman = models.CharField(max_length=120, blank=True, null=True)
    tshirt = models.CharField(max_length=120, blank=True, null=True)
    raket = models.CharField(max_length=120, blank=True, null=True)
