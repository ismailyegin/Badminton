from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect

from sbs.models import *
from sbs.models.FedsportalModels import Sporcular, Turnuvalar, TurnSporculari, TurnHakemleri
from sbs.models.EnumFields import EnumFields
from sbs.models.Material import Material
from sbs.services import general_methods

from sbs.models.CompetitionsAthlete import CompetitionsAthlete

from sbs.models.Category import Category

from datetime import date, datetime


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
    # print(eskihakemler.count())
    for e in eskihakemler :
        # print(e.adi + " " + e.soyadi)
        user = User(
            first_name=e.adi,
            last_name=e.soyadi,
            email=e.eposta if e.eposta else 'badminton@hotmail.com',
            username=e.tcno

                    )
        user.save()

        # print(user)
        grup = Group.objects.get(name='Hakem')
        user.groups.add(grup)
        # print(grup)
        meterial = Meterial(ayakkabi=e.ayakkabi,
                            esofman=e.esofman,
                            tshirt=e.tshirt,
                            raket=e.raket
                            )
        meterial.save()
        # print(meterial)
        # print(e.egitimid)
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

        # print(person)
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
        # print(comikamet)
        # print(comev)
        # print(comis)
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
    # print(eskihakemler.count())

    grup = Group.objects.get(name='Antrenor')
    # print(grup)
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

            # print(user)
            user.groups.add(grup)
            # print(grup)
            meterial = Meterial(ayakkabi=e.ayakkabi,
                                esofman=e.esofman,
                                tshirt=e.tshirt,
                                raket=e.raket
                                )
            meterial.save()
            # print(meterial)
            # print(e.egitimid)
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
            # print(person)

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
            # print(comikamet)
            # print(comev)
            # print(comis)
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

    # grup = Group.objects.get(name='Sporcu')
    # print(grup)
    # for e in eskihakemler:
    #
    #     if User.objects.filter(username=e.tcno):
    #         if User.objects.filter(username=e.tcno)[0].groups.filter(name="Hakem"):
    #             if not (Athlete.objects.filter(user=User.objects.filter(username=e.tcno)[0])):
    #                 judge = Judge.objects.get(user=User.objects.filter(username=e.tcno)[0])
    #                 print(e.adi + " " + e.soyadi)
    #                 athlete = Athlete(
    #                     user=judge.user,
    #                     communication=judge.communication,
    #                     communicationHome=judge.communicationHome,
    #                     communicationJop=judge.communicationJop,
    #                     iban=judge.iban,
    #                     oldpk=judge.oldpk,
    #                     person=judge.person
    #
    #                 )
    #                 athlete.save()
    #                 athlete.user.groups.add(grup)
    #                 athlete.save()
    #             else:
    #                 print('Control Hakem')
    #         elif User.objects.filter(username=e.tcno)[0].groups.filter(name="Antrenor"):
    #             if not (Athlete.objects.filter(user=User.objects.filter(username=e.tcno)[0])):
    #                 coach = Coach.objects.get(user=User.objects.filter(username=e.tcno)[0])
    #                 athlete = Athlete(
    #                     user=coach.user,
    #                     communication=coach.communication,
    #                     communicationHome=coach.communicationHome,
    #                     communicationJop=coach.communicationJop,
    #                     iban=coach.iban,
    #                     oldpk=coach.oldpk,
    #                     person=coach.person
    #
    #                 )
    #                 athlete.save()
    #                 athlete.user.groups.add(grup)
    #                 athlete.save()
    #             else:
    #                 print('Control Antrenor')
    #
    #
    #
    #     else:
    #         user = User(
    #             first_name=e.adi,
    #             last_name=e.soyadi,
    #             email=e.eposta if e.eposta else 'badminton@hotmail.com',
    #             username=e.tcno
    #
    #         )
    #         user.save()
    #
    #         # print(user)
    #         user.groups.add(grup)
    #         # print(grup)
    #         meterial = Meterial(ayakkabi=e.ayakkabi,
    #                             esofman=e.esofman,
    #                             tshirt=e.tshirt,
    #                             raket=e.raket
    #                             )
    #         meterial.save()
    #         # print(meterial)
    #         # print(e.egitimid)
    #         person = Person(
    #             tc=e.tcno,
    #             birthplace=e.dogumyeri,
    #             motherName=e.anneadi,
    #             fatherName=e.babaadi,
    #             birthDate=e.dogumtarihi,
    #             bloodType=e.kangrubu,
    #             # profileImage=e.resim,
    #             gender=e.cinsiyet,
    #             uyrukid=e.uyrukid,
    #             nufus_ailesirano=e.nufus_ailesirano,
    #             nufus_ciltno=e.nufus_ciltno,
    #             nufus_sirano=e.nufus_sirano,
    #             meslek=e.meslek,
    #             kurum=e.kurum,
    #             is_unvani=e.is_unvani,
    #             # meterial=meterial.id,
    #             # education=e.egitimid
    #
    #         )
    #
    #         person.material = meterial
    #         person.save()
    #         # print(person)
    #
    #         comikamet = Communication(
    #             phoneNumber=e.ceptel,
    #             address=e.yerlesimyeri,
    #             city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
    #             country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
    #         )
    #         comikamet.save()
    #         comev = Communication(
    #             phoneNumber=e.ceptel,
    #             phoneNumber2=e.evtel,
    #             address=e.ev_adresi,
    #             city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
    #             country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
    #         )
    #         comev.save()
    #         comis = Communication(
    #             phoneNumber=e.ceptel,
    #             phoneNumber2=e.istel,
    #             address=e.is_adresi,
    #             city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
    #             country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
    #         )
    #         comis.save()
    #         # print(comikamet)
    #         # print(comev)
    #         # print(comis)
    #         athlete = Athlete(
    #             pk=e.sporcuid,
    #             person=person,
    #             communication=comikamet,
    #             communicationHome=comev,
    #             communicationJop=comis,
    #             user=user,
    #             iban=e.bankahesapno,
    #             oldpk=e.sporcuid
    #         )
    #         athlete.save()

    return redirect('sbs:admin')


@login_required
def lisans_aktar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    eskihakemler = Sporcular.objects.exclude(kulupid=None).exclude(tcno=None).filter(sporcu=1)
    print(eskihakemler.count())
    for item in eskihakemler:

        athlete = Athlete.objects.get(oldpk=item.sporcuid)
        if athlete.licenses.count() == 0:
            lisans = License(

                licenseNo=item.lisansno,
                branch=EnumFields.BADMİNTON.value,
                isActive=True,
                status=License.APPROVED
            )
            if item.lisanstarihi is not None:
                lisans.expireDate = item.lisanstarihi
                lisans.startDate = date(int(item.lisanstarihi.year) - 1, item.lisanstarihi.month, item.lisanstarihi.day)

            if item.kulupid is not None:
                lisans.sportsClub = SportsClub.objects.get(pk=item.kulupid.pk)
            if item.antrenorid is not None:
                if Coach.objects.filter(oldpk=item.antrenorid.pk):
                    lisans.coach = Coach.objects.get(oldpk=item.antrenorid.pk)
            if item.antrenorid2 is not None:
                if Coach.objects.filter(oldpk=item.antrenorid2.pk):
                    lisans.coach2 = Coach.objects.get(oldpk=item.antrenorid2.pk)
            lisans.save()
            athlete.licenses.add(lisans);

    return redirect('sbs:admin')


@login_required
def control(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    print(Sporcular.objects.filter(sporcu=1).exclude(kulupid=None).exclude(tcno=None).count())
    for item in Sporcular.objects.filter(sporcu=1).exclude(kulupid=None).exclude(tcno=None):
        athlete = Athlete.objects.get(oldpk=item.sporcuid)
        if athlete.licenses.count() > 1:
            print(item.adi + " " + item.soyadi)
            for lisans in athlete.licenses.all():

                athlete.licenses.remove(lisans)
                lisans.delete()
                if athlete.licenses.count() == 1:
                    break;

        elif athlete.licenses.count() == 0:
            print(item.adi + "---" + item.soyadi)
            lisans = License(

                licenseNo=item.lisansno,
                branch=EnumFields.BADMİNTON.value,
                isActive=True,
                status=License.APPROVED
            )
            if item.lisanstarihi is not None:
                lisans.expireDate = item.lisanstarihi
                lisans.startDate = date(int(item.lisanstarihi.year) - 1, item.lisanstarihi.month, item.lisanstarihi.day)

            if item.kulupid is not None:
                lisans.sportsClub = SportsClub.objects.get(pk=item.kulupid.pk)
            if item.antrenorid is not None:
                if Coach.objects.filter(oldpk=item.antrenorid.pk):
                    lisans.coach = Coach.objects.get(oldpk=item.antrenorid.pk)
            if item.antrenorid2 is not None:
                if Coach.objects.filter(oldpk=item.antrenorid2.pk):
                    lisans.coach2 = Coach.objects.get(oldpk=item.antrenorid2.pk)
            lisans.save()
            athlete.licenses.add(lisans);
            athlete.save()







    return redirect('sbs:admin')


@login_required
def kademe_aktar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    antrenor = Sporcular.objects.exclude(tcno=None).filter(antrenor=1)

    for item in antrenor:

        coach = Coach.objects.get(oldpk=item.sporcuid)

        print(coach.user.get_full_name())
        print(item.antrenorkademeid)
        print(item.antrenorvize)

        if item.antrenorkademeid:
            grade = Level(definition=CategoryItem.objects.get(name=item.antrenorkademeid),
                          branch=EnumFields.BADMİNTON.value)
            grade.levelType = EnumFields.LEVELTYPE.GRADE
            grade.status = Level.APPROVED
            grade.save()
            coach.grades.add(grade)
            coach.save()

        if item.antrenorvize:
            visa = Level(branch=EnumFields.BADMİNTON.value)
            visa.startDate = item.antrenorvize
            visa.definition = CategoryItem.objects.get(forWhichClazz='VISA')
            visa.levelType = EnumFields.LEVELTYPE.VISA
            visa.status = Level.APPROVED
            visa.isActive = True
            visa.save()
            coach.visa.add(visa)
            coach.save()




    return redirect('sbs:admin')


@login_required
def username_aktar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    users = User.objects.all()
    for item in users:
        if item.email != "badminton@hotmail.com":
            if not User.objects.filter(username=item.email):
                if item.username != item.email:
                    item.username = item.email
                    item.save()

    return redirect('sbs:admin')


@login_required
def musabaka_aktar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    competities = Turnuvalar.objects.all()

    for item in competities:
        print(item.turnuvaadi)

        competi = Competition(

            pk=item.turnuvaid,
            name=item.turnuvaadi,
            startDate=item.basltarihi,
            finishDate=item.bitistarihi,
            registerStartDate=item.basvurubasltarihi,
            registerFinishDate=item.basvurubitistarihi,
            explanation=item.aciklama

        )
        competi.save()

    print(competities.count())

    return redirect('sbs:admin')


@login_required
def musabaka_sporcu_aktar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    turn = TurnSporculari.objects.all()

    for item in turn:

        com = CompetitionsAthlete(pk=item.turnsporcuid)

        if not CompetitionsAthlete.objects.filter(pk=item.turnsporcuid):
            if item.antrenorid:
                com.coach = Coach.objects.get(oldpk=item.antrenorid)
            if item.kulupid:
                com.club = SportsClub.objects.get(pk=item.kulupid)
            if item.sporcuid:
                com.athlete = Athlete.objects.get(oldpk=item.sporcuid.pk)
            if item.turnuvaid:
                com.competition = Competition.objects.get(pk=item.turnuvaid.pk)
            if item.kategoriid:
                com.category = Category.objects.get(pk=item.kategoriid.pk)
            if item.sira:
                com.sira = item.sira
            if item.grupid:
                com.grupid = item.grupid

            com.save()

    print(com.count())

    return redirect('sbs:admin')
