from django import forms
from django.forms import ModelForm

from sbs.models import Communication


class CommunicationWorkForm(ModelForm):
    class Meta:
        model = Communication

        fields = (
            'phoneNumber', 'address', 'postalCode', 'phoneNumber2', 'city', 'country')
        labels = {'phoneNumber': 'Cep Telefonu', 'phoneNumber2': 'İş Telefonu', 'postalCode': 'Posta Kodu',
                  'city': 'İl', 'country': 'Ülke'}
        widgets = {

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2', 'name': 'adressWork', 'id': 'adressWork', }),

            'phoneNumber': forms.TextInput(
                attrs={'class': 'form-control ', 'name': 'phoneNumber', 'id': 'phoneNumber', }),

            'phoneNumber2': forms.TextInput(
                attrs={'class': 'form-control ', 'name': 'phoneNumber2Work', 'id': 'phoneNumber2Work', }),

            'postalCode': forms.TextInput(
                attrs={'class': 'form-control ', 'name': 'postalCodeWork', 'id': 'postalCodeWork', }),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'name': 'cityWork', 'id': 'cityWork',
                                        'style': 'width: 100%;', 'required': 'required'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'name': 'countryWork', 'id': 'countryWork',
                                           'style': 'width: 100%;', 'required': 'required'}),

        }
