from django import forms
from django.forms import ModelForm

from sbs.models import Communication


class CommunicationForm(ModelForm):
    class Meta:
        model = Communication

        fields = (
            'phoneNumber', 'address', 'postalCode', 'phoneNumber2', 'city', 'country', 'phoneHome', 'phoneJop',
            'addressHome', 'addressJop')
        labels = {'phoneNumber': 'Cep Telefonu',
                  'phoneNumber2': 'Sabit Telefon',
                  'phoneHome': 'Ev Telefonu',
                  'phoneJop': 'İş Telefonu',
                  'addressHome': 'Ev Adresi',
                  'addressJop': 'İş Adresi',
                  'postalCode': 'Posta Kodu',
                  'city': 'İl', 'country': 'Ülke'}
        widgets = {

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2'}),
            'addressHome': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2'}),
            'addressJop': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2'}),

            'phoneNumber': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'phoneNumber2': forms.TextInput(attrs={'class': 'form-control '}),

            'postalCode': forms.TextInput(attrs={'class': 'form-control '}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;', 'required': 'required'}),

            'phoneHome': forms.TextInput(attrs={'class': 'form-control '}),

            'phoneJop': forms.TextInput(attrs={'class': 'form-control '}),

        }
