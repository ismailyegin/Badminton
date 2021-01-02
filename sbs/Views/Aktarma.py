from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from sbs.models import FedsportalModels, SportsClub, Communication, City, Country
from sbs.services import general_methods


@login_required
def kulup_aktar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    eskikulupler=FedsportalModels.Kulupler.objects.all()
    for e in eskikulupler :
        citya = City.objects.get(pk=e.ilid.pk)
        country=Country.objects.get(pk=1)
        c = Communication(address=e.adres1,phoneNumber=e.telefon,city=citya,country=country)
        c.save()
        s = SportsClub(pk=e.kulupid,name=e.kulupadi,foundingDate=e.tesciltarihi,clubMail=e.eposta,communication=c)

        s.save()

@login_required
def hakem_aktar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    eskihakemler=FedsportalModels.Sporcular.objects.all()
    for e in eskihakemler :
        citya = City.objects.get(pk=e.ilid.pk)
        country=Country.objects.get(pk=1)
        c = Communication(address=e.adres1,phoneNumber=e.telefon,city=citya,country=country)
        c.save()
        s = SportsClub(pk=e.kulupid,name=e.kulupadi,foundingDate=e.tesciltarihi,clubMail=e.eposta,communication=c)

        s.save()
