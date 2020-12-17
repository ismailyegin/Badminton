from django.db import models


class Products(models.Model):
    RAKETLER = 'RAKET'
    TOPLAR = 'TOPLAR'
    AYAKKABI = 'AYAKKABI'
    ÇANTA = 'ÇANTA'
    AKSESUAR = 'AKSESUAR'
    GRİP = 'GRİP'
    KORDAJ = 'KORDAJ'
    EKİPMAN = 'EKİPMAN'
    KIYAFET = 'KIYAFET'

    Category = (
        (RAKETLER, 'RAKET'),
        (TOPLAR, 'TOPLAR'),
        (AYAKKABI, 'AYAKKABI'),
        (ÇANTA, 'ÇANTA'),
        (AKSESUAR, 'AKSESUAR'),
        (GRİP, 'GRİP'),
        (KORDAJ, 'KORDAJ'),
        (EKİPMAN, 'EKİPMAN'),
        (KIYAFET, 'KIYAFET'),

    )

    name = models.CharField(max_length=120, null=False, blank=False)
    category = models.CharField(max_length=128, verbose_name='category', choices=Category, null=True, blank=True)
    stock = models.IntegerField()
    suppeliers = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
