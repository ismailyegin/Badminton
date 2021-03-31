from django import forms
from django.forms import ModelForm


from sbs.models.Claim import Claim


class DestekSearchform(ModelForm):
    class Meta:
        model = Claim


        fields = (
             'status',  'importanceSort')

        labels = {

                  'status': 'Durumu ',
                  'importanceSort': 'Önem Durumu',
                  }

        widgets = {
            'status': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),
            'importanceSort': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                  'style': 'width: 100%; '}),



        }
