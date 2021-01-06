from django import forms
from django.forms import ModelForm

from sbs.models import Communication


class CommunicationHomeForm(ModelForm):
    class Meta:
        model = Communication

        fields = (
            'phoneNumber', 'address', 'postalCode', 'phoneNumber2', 'city', 'country')
        labels = {'phoneNumber': 'Cep Telefonu', 'phoneNumber2': 'Ev Telefonu', 'postalCode': 'Posta Kodu',
                  'city': 'İl', 'country': 'Ülke'}
        widgets = {

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2', 'name': 'adressHome', 'id': 'adresHome', }),

            'phoneNumber': forms.TextInput(
                attrs={'class': 'form-control ', 'name': 'phoneNumberHome', 'id': 'phone_numberHome'}),

            'phoneNumber2': forms.TextInput(
                attrs={'class': 'form-control ', 'name': 'phoneNumber2Home', 'id': 'phone_number2Home'}),

            'postalCode': forms.TextInput(
                attrs={'class': 'form-control', 'name': 'postacodeHome', 'id': 'postacodeHome'}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'name': 'cityHome', 'id': 'cityHome',
                                        'style': 'width: 100%;', 'required': 'required'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'name': 'countryHome', 'id': 'countryHome',
                                           'style': 'width: 100%;', 'required': 'required'}),

        }
