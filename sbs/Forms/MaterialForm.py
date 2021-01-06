from django import forms
from django.forms import ModelForm

from sbs.models.Material import Material


class MaterialForm(ModelForm):
    class Meta:
        model = Material

        fields = (
            'ayakkabi', 'esofman', 'tshirt', 'raket')
        labels = {'raket': 'Raket', 'tshirt': 'Tshirt', 'esofman': 'Esofman', 'ayakkabi': 'Ayakkabi'}
        widgets = {

            'ayakkabi': forms.TextInput(attrs={'class': 'form-control '}),

            'esofman': forms.TextInput(attrs={'class': 'form-control '}),

            'tshirt': forms.TextInput(attrs={'class': 'form-control '}),

            'raket': forms.TextInput(attrs={'class': 'form-control '}),

        }
