from django import forms
from django.forms import ModelForm

from sbs.models import Competition


class CompetitionForm(ModelForm):
    class Meta:
        model = Competition

        fields = (
            'name', 'startDate', 'finishDate', 'compType', 'eventPlace',
            'registerStartDate', 'registerFinishDate',)

        labels = {'name': 'İsim', 'startDate': 'Başlangıç Tarihi', 'finishDate': 'Bitiş Tarihi',
                  'eventPlace': 'Etkinlik Yeri',
                  'registerStartDate': 'Ön Kayıt Başlangıç Tarihi',
                  'registerFinishDate': 'Ön Kayıt Bitiş Tarihi', }

        widgets = {

            'registerStartDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'registerFinishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),

            'eventPlace': forms.TextInput(attrs={'class': 'form-control'}),

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker2', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required'}),

            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker4', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required'}),

            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

        }
