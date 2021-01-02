from sbs.models import *
from sbs.models.FedsportalModels import Sporcular, Iller, Users
from sbs.services import general_methods

from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect


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

    eskihakemler = Sporcular.objects.filter(hakem=1)
    print(eskihakemler.count())
    for e in eskihakemler :
        print(e.adi + " " + e.soyadi)
        user = User(first_name=e.adi,
                    last_name=e.soyadi,
                    email=e.eposta,
                    username=e.user.user_name

                    )
        print(user)
        grup = Group.objects.get(name='Hakem')
        print(grup)
        person = Person(tc=e.tcno,
                        birthplace=e.dogumyeri,
                        motherName=e.anneadi,
                        fatherName=e.babaadi,
                        birthDate=e.dogumtarihi,
                        bloodType=e.kangrubu,
                        profileImage=e.resim,
                        )
        # if e.nufus_ilid.iladi:
        #     print(e.nufus_ilid.iladi)
        com = Communication(
            phoneNumber=e.ceptel,
            phoneNumber2=e.evtel,
            address=e.is_adresi,
            city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
            country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
        )
        print(com)
        # hakem=Judge(
        #     pk=e.sporcuid
        #     person=person,
        #     communication=com,
        #     user=user,
        #     iban=e.bankahesapno,
        #
        #
        # )

    return redirect('sbs:admin')
