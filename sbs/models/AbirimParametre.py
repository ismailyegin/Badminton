from django.db import models

from sbs.models.Abirim import Abirim
from sbs.models.Aevrak import Aevrak
from sbs.services import general_methods
from unicode_tr import unicode_tr


class AbirimParametre(models.Model):
    aDate = 'date'
    aString = 'string'
    aNumber = 'number'
    aYear='year'

    Type = (
        (aDate, 'Tarih'),
        (aString, 'Metin'),
        (aNumber, 'Sayi'),
        ( aYear,'Yil')

    )

    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=120,  null=True, blank=True, verbose_name='Başlık')
    type = models.CharField(max_length=128, verbose_name='Türü ', choices=Type,default=aString)
    birim = models.ForeignKey(Abirim, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Birim')

    def __str__(self):
        return '%s' % (self.title)


    def save(self, force_insert=False, force_update=False):
        if self.title:
            self.title = unicode_tr(self.title)
            self.title = self.title.upper()

        super(AbirimParametre, self).save(force_insert, force_update)