from django.db import models
from django.contrib import admin

class CompetitionAges(models.Model):
    year = models.IntegerField(blank=False, null=False,unique=True)
    def __str__(self):
        return '%s ' % self.year

admin.site.register(CompetitionAges)