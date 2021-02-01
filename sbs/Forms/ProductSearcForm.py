from django import forms
from django.forms import ModelForm

from sbs.models.Deposit import Deposit


class ProductSearhForm(ModelForm):
    class Meta:
        model = Deposit

        fields = (
            'product', 'club', 'date')

        labels = {'product': 'Ürün İsmi ', 'club': 'Kulüp',
                  'date': 'Tarih',
                  }

        widgets = {

            'product': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%; '}),

            'club': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; '}),
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false'}),

        }

    def __init__(self, *args, **kwargs):
        super(ProductSearhForm, self).__init__(*args, **kwargs)
        self.fields['date'].required = False
