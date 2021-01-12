from django import forms
from django.forms import ModelForm

from sbs.models import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person

        fields = (
            'tc', 'profileImage',
            'height', 'weight',
            'birthDate', 'bloodType',
            'gender', 'birthplace',
            'motherName',
            'profileImage', 'fatherName',
            'meslek', 'kurum', 'is_unvani',
            'education', 'mezunokul',
            'uyrukid', 'nufus_ailesirano',
            'nufus_sirano', 'nufus_ciltno')

        labels = {'tc': 'T.C.',
                  'gender': 'Cinsiyet',
                  'profileImage': 'Profil Resmi',
                  'uyrukid': 'Uyruk ',
                  'nufus_ailesirano': 'Nufus Aile Sıra No',
                  'nufus_sirano': 'Nufus Sıra No',
                  'nufus_ciltno': 'Nufus Cilt No',
                  'kurum': 'kurum',
                  'is_unvani': 'İs Unvanı ',
                  'education': 'Eğitim',
                  'mezunokul': 'Mezun Okul ',
                  'meslek': 'Meslek',
                  'height': 'Boy',
                  'weight': 'Kilo',

                  }

        widgets = {

            'profileImage': forms.FileInput(),

            'uyrukid': forms.TextInput(attrs={'class': 'form-control '}),

            'is_unvani': forms.TextInput(attrs={'class': 'form-control '}),

            'nufus_ailesirano': forms.TextInput(attrs={'class': 'form-control'}),

            'nufus_sirano': forms.TextInput(attrs={'class': 'form-control'}),

            'nufus_ciltno': forms.TextInput(attrs={'class': 'form-control ', }),

            'kurum': forms.TextInput(attrs={'class': 'form-control'}),

            'meslek': forms.TextInput(attrs={'class': 'form-control'}),

            'tc': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'height': forms.TextInput(attrs={'class': 'form-control'}),

            'weight': forms.TextInput(attrs={'class': 'form-control'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': ''}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': ''}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

            'bloodType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; '}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;', 'required': 'required'}),
            'education': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%;'}),
            'mezunokul': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def clean_tc(self):

        data = self.cleaned_data['tc']
        print(self.instance)
        if self.instance is None:
            if Person.objects.filter(tc=data).exists():
                raise forms.ValidationError("This tc already used")
            return data
        else:
            return data
