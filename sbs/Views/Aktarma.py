from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect

from sbs.models import *
from sbs.models.FedsportalModels import Sporcular
from sbs.models.Material import Meterial
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

    eskihakemler = Sporcular.objects.filter(hakem=1)
    print(eskihakemler.count())
    for e in eskihakemler :
        print(e.adi + " " + e.soyadi)
        user = User(
            first_name=e.adi,
                    last_name=e.soyadi,
            email=e.eposta if e.eposta else 'badminton@hotmail.com',
            username=e.tcno

                    )
        user.save()


        print(user)
        grup = Group.objects.get(name='Hakem')
        user.groups.add(grup)
        print(grup)
        meterial = Meterial(ayakkabi=e.ayakkabi,
                            esofman=e.esofman,
                            tshirt=e.tshirt,
                            raket=e.raket
                            )
        meterial.save()
        print(meterial)
        print(e.egitimid)
        person = Person(
            tc=e.tcno,
            birthplace=e.dogumyeri,
            motherName=e.anneadi,
            fatherName=e.babaadi,
            birthDate=e.dogumtarihi,
            bloodType=e.kangrubu,
            # profileImage=e.resim,
            gender=e.cinsiyet,
            uyrukid=e.uyrukid,
            nufus_ailesirano=e.nufus_ailesirano,
            nufus_ciltno=e.nufus_ciltno,
            nufus_sirano=e.nufus_sirano,
            meslek=e.meslek,
            kurum=e.kurum,
            is_unvani=e.is_unvani,
            # meterial=meterial.id,
            # education=e.egitimid

        )

        print(person)
        person.material = meterial
        person.save()

        comikamet = Communication(
            phoneNumber=e.ceptel,
            address=e.yerlesimyeri,
            city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
            country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
        )
        comikamet.save()
        comev = Communication(
            phoneNumber=e.ceptel,
            phoneNumber2=e.evtel,
            address=e.ev_adresi,
            city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
            country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
        )
        comev.save()
        comis = Communication(
            phoneNumber=e.ceptel,
            phoneNumber2=e.istel,
            address=e.is_adresi,
            city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
            country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
        )
        comis.save()
        print(comikamet)
        print(comev)
        print(comis)
        hakem = Judge(
            pk=e.sporcuid,
            person=person,
            communication=comikamet,
            communicationHome=comev,
            communicationJop=comis,
            user=user,
            iban=e.bankahesapno,
            oldpk=e.sporcuid
        )
        hakem.save()

    return redirect('sbs:admin')


@login_required
def antrenor_aktar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    eskihakemler = Sporcular.objects.filter(antrenor=1).exclude(tcno=None)
    print(eskihakemler.count())

    grup = Group.objects.get(name='Antrenor')
    print(grup)
    for e in eskihakemler:
        print(e.adi + " " + e.soyadi)
        if User.objects.filter(username=e.tcno):
            if User.objects.filter(username=e.tcno)[0].groups.filter(name="Hakem"):
                if not (Coach.objects.filter(user=User.objects.filter(username=e.tcno)[0])):
                    judge = Judge.objects.get(user=User.objects.filter(username=e.tcno)[0])
                    user = judge.user
                    coach = Coach(
                        user=judge.user,
                        communication=judge.communication,
                        communicationHome=judge.communicationHome,
                        communicationJop=judge.communicationJop,
                        iban=judge.iban,
                        oldpk=judge.oldpk,
                        person=judge.person

                    )
                    coach.save()
                    coach.user.groups.add(grup)
                    coach.save()
                else:
                    print('deger eklenmiş')


        else:
            user = User(
                first_name=e.adi,
                last_name=e.soyadi,
                email=e.eposta if e.eposta else 'badminton@hotmail.com',
                username=e.tcno

            )
            user.save()

            print(user)
            user.groups.add(grup)
            print(grup)
            meterial = Meterial(ayakkabi=e.ayakkabi,
                                esofman=e.esofman,
                                tshirt=e.tshirt,
                                raket=e.raket
                                )
            meterial.save()
            print(meterial)
            print(e.egitimid)
            person = Person(
                tc=e.tcno,
                birthplace=e.dogumyeri,
                motherName=e.anneadi,
                fatherName=e.babaadi,
                birthDate=e.dogumtarihi,
                bloodType=e.kangrubu,
                # profileImage=e.resim,
                gender=e.cinsiyet,
                uyrukid=e.uyrukid,
                nufus_ailesirano=e.nufus_ailesirano,
                nufus_ciltno=e.nufus_ciltno,
                nufus_sirano=e.nufus_sirano,
                meslek=e.meslek,
                kurum=e.kurum,
                is_unvani=e.is_unvani,
                # meterial=meterial.id,
                # education=e.egitimid

            )

            person.material = meterial
            person.save()
            print(person)

            comikamet = Communication(
                phoneNumber=e.ceptel,
                address=e.yerlesimyeri,
                city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
                country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
            )
            comikamet.save()
            comev = Communication(
                phoneNumber=e.ceptel,
                phoneNumber2=e.evtel,
                address=e.ev_adresi,
                city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
                country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
            )
            comev.save()
            comis = Communication(
                phoneNumber=e.ceptel,
                phoneNumber2=e.istel,
                address=e.is_adresi,
                city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
                country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
            )
            comis.save()
            print(comikamet)
            print(comev)
            print(comis)
            coach = Coach(
                pk=e.sporcuid,
                person=person,
                communication=comikamet,
                communicationHome=comev,
                communicationJop=comis,
                user=user,
                iban=e.bankahesapno,
                oldpk=e.sporcuid
            )
            coach.save()

    return redirect('sbs:admin')


@login_required
def sporcu_aktar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    eskihakemler = Sporcular.objects.filter(sporcu=1).exclude(tcno=None)
    print(eskihakemler.count())

    grup = Group.objects.get(name='Sporcu')
    print(grup)
    for e in eskihakemler:
        print(e.adi + " " + e.soyadi)
        if User.objects.filter(username=e.tcno):
            if User.objects.filter(username=e.tcno)[0].groups.filter(name="Hakem"):
                if not (Coach.objects.filter(user=User.objects.filter(username=e.tcno)[0])):
                    judge = Judge.objects.get(user=User.objects.filter(username=e.tcno)[0])
                    coach = Coach(
                        user=judge.user,
                        communication=judge.communication,
                        communicationHome=judge.communicationHome,
                        communicationJop=judge.communicationJop,
                        iban=judge.iban,
                        oldpk=judge.oldpk,
                        person=judge.person

                    )
                    coach.save()
                    coach.user.groups.add(grup)
                    coach.save()
                else:
                    print('Control Hakem')
            elif User.objects.filter(username=e.tcno)[0].groups.filter(name="Antrenor"):
                if not (Athlete.objects.filter(user=User.objects.filter(username=e.tcno)[0])):
                    coach = Coach.objects.get(user=User.objects.filter(username=e.tcno)[0])
                    athlete = Athlete(
                        user=coach.user,
                        communication=coach.communication,
                        communicationHome=coach.communicationHome,
                        communicationJop=coach.communicationJop,
                        iban=coach.iban,
                        oldpk=coach.oldpk,
                        person=coach.person

                    )
                    athlete.save()
                    athlete.user.groups.add(grup)
                    athlete.save()
                else:
                    print('Control Antrenor')



        else:
            user = User(
                first_name=e.adi,
                last_name=e.soyadi,
                email=e.eposta if e.eposta else 'badminton@hotmail.com',
                username=e.tcno

            )
            user.save()

            print(user)
            user.groups.add(grup)
            print(grup)
            meterial = Meterial(ayakkabi=e.ayakkabi,
                                esofman=e.esofman,
                                tshirt=e.tshirt,
                                raket=e.raket
                                )
            meterial.save()
            print(meterial)
            print(e.egitimid)
            person = Person(
                tc=e.tcno,
                birthplace=e.dogumyeri,
                motherName=e.anneadi,
                fatherName=e.babaadi,
                birthDate=e.dogumtarihi,
                bloodType=e.kangrubu,
                # profileImage=e.resim,
                gender=e.cinsiyet,
                uyrukid=e.uyrukid,
                nufus_ailesirano=e.nufus_ailesirano,
                nufus_ciltno=e.nufus_ciltno,
                nufus_sirano=e.nufus_sirano,
                meslek=e.meslek,
                kurum=e.kurum,
                is_unvani=e.is_unvani,
                # meterial=meterial.id,
                # education=e.egitimid

            )

            person.material = meterial
            person.save()
            print(person)

            comikamet = Communication(
                phoneNumber=e.ceptel,
                address=e.yerlesimyeri,
                city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
                country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
            )
            comikamet.save()
            comev = Communication(
                phoneNumber=e.ceptel,
                phoneNumber2=e.evtel,
                address=e.ev_adresi,
                city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
                country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
            )
            comev.save()
            comis = Communication(
                phoneNumber=e.ceptel,
                phoneNumber2=e.istel,
                address=e.is_adresi,
                city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
                country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
            )
            comis.save()
            print(comikamet)
            print(comev)
            print(comis)
            athlete = Athlete(
                pk=e.sporcuid,
                person=person,
                communication=comikamet,
                communicationHome=comev,
                communicationJop=comis,
                user=user,
                iban=e.bankahesapno,
                oldpk=e.sporcuid
            )
            athlete.save()

    return redirect('sbs:admin')
