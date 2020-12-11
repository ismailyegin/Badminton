from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
# from rest_framework_simplejwt import views as jwt_views
from django.http import JsonResponse

from sbs.models import SportClubUser, SportsClub, Coach, Level, License, Athlete, Person, Judge
from sbs.services import general_methods

from sbs.models.ReferenceCoach import ReferenceCoach
from sbs.models.ReferenceReferee import ReferenceReferee
from sbs.models.PreRegistration import PreRegistration
# from rest_framework.authtoken.models import Token
from sbs.models.ActiveGroup import ActiveGroup

from datetime import date, datetime


@login_required
def return_message(request):
    return render(request, 'Chat/chat.html')



@login_required
def return_athlete_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'anasayfa/sporcu.html')


@login_required
def return_referee_dashboard(request):
    perm = general_methods.control_access_judge(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = User.objects.get(pk=request.user.pk)
    judge = Judge.objects.get(user=user)
    return render(request, 'anasayfa/hakem.html', {'user': user, 'judge': judge})


@login_required
def return_coach_dashboard(request):
    perm = general_methods.control_access_klup(request)
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    coach = Coach.objects.get(user=user)
    clup = SportsClub.objects.filter(coachs=coach)
    clupsPk = []
    for item in clup:
        clupsPk.append(item.pk)
    athletes = Athlete.objects.filter(licenses__sportsClub_id__in=clupsPk).distinct()
    athletes |= Athlete.objects.filter(licenses__coach=coach).distinct()

    athlete_count = athletes.count()

    return render(request, 'anasayfa/antrenor.html', {'athlete_count': athlete_count})


@login_required
def return_directory_dashboard(request):
    group = request.user.groups.all()[0]
    if not group.name == "Yonetim":
        logout(request)
        return redirect('accounts:login')
    return render(request, 'anasayfa/federasyon.html')


@login_required
def return_club_user_dashboard(request):
    perm = general_methods.control_access_klup(request)
    # x = general_methods.import_csv()

    if not perm:
        logout(request)
        return redirect('accounts:login')

    if not perm:
        logout(request)
        return redirect('accounts:login')

    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    current_user = request.user
    clubuser = SportClubUser.objects.get(user=current_user)
    club = SportsClub.objects.filter(clubUser=clubuser)[0]


    total_club_user = club.clubUser.count()
    total_coach = Coach.objects.filter(sportsclub=club).count()
    sc_user = SportClubUser.objects.get(user=user)
    clubsPk = []
    clubs = SportsClub.objects.filter(clubUser=sc_user)
    for club in clubs:
        clubsPk.append(club.pk)
    total_athlete = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct().count()

    # Sporcu bilgilerinde eksik var mı diye control
    athletes = Athlete.objects.none()
    if user.groups.filter(name='KulupUye'):
        sc_user = SportClubUser.objects.get(user=user)
        if sc_user.dataAccessControl == False or sc_user.dataAccessControl == None:
            clubsPk = []
            clubs = SportsClub.objects.filter(clubUser=sc_user)
            for club in clubs:
                if club.dataAccessControl == False or club.dataAccessControl is None:
                    clubsPk.append(club.pk)
            # print(len(clubsPk))
            if len(clubsPk) != 0:
                athletes = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct()
                athletes = athletes.filter(user__last_name='') | athletes.filter(user__first_name='') | athletes.filter(
                    user__email='') | athletes.filter(person__tc='') | athletes.filter(
                    person__birthDate=None) | athletes.filter(
                    person__gender=None) | athletes.filter(person__birthplace='') | athletes.filter(
                    person__motherName='') | athletes.filter(person__fatherName='') | athletes.filter(
                    communication__city__name='') | athletes.filter(communication__country__name='')
                # false degerinde clubun eksigi yok anlamında kulanilmistir.
                for club in clubs:
                    if athletes:
                        club.dataAccessControl = False
                        club.save()

                    else:

                        club.dataAccessControl = True
                        club.save()

                if athletes:
                    sc_user.dataAccessControl = False

                else:
                    sc_user.dataAccessControl = True

                sc_user.save()


            else:
                sc_user.dataAccessControl = True
                sc_user.save()

    return render(request, 'anasayfa/kulup-uyesi.html',
                  {'total_club_user': total_club_user, 'total_coach': total_coach,
                   'total_athlete': total_athlete, 'athletes': athletes})


@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    # x = general_methods.import_csv()

    if not perm:
        logout(request)
        return redirect('accounts:login')

    # son eklenen 8 sporcuyu ekledik
    last_athlete = Athlete.objects.order_by('-creationDate')[:8]
    total_club = SportsClub.objects.all().count()
    total_athlete = Athlete.objects.all().count()
    total_athlete_gender_man = Athlete.objects.filter(person__gender=Person.MALE).count()
    total_athlete_gender_woman = Athlete.objects.filter(person__gender=Person.FEMALE).count()
    total_athlate_last_month = Athlete.objects.exclude(user__date_joined__month=datetime.now().month).count()
    total_club_user = SportClubUser.objects.all().count()
    total_coachs = Coach.objects.all().count()
    total_judge = Judge.objects.all().count()
    total_user = User.objects.all().count()

    # total_notifications_refere = ReferenceReferee.objects.filter(status=ReferenceReferee.WAITED).count()
    # total_notifications_coach = ReferenceReferee.objects.filter(status=ReferenceCoach.WAITED).count()
    # total_notifications_clup = PreRegistration.objects.filter(status=PreRegistration.WAITED).count()
    # notifications_tatal = total_notifications_refere + total_notifications_coach + total_notifications_clup

    return render(request, 'anasayfa/admin.html',
                  {'total_club_user': total_club_user, 'total_club': total_club,
                   'total_athlete': total_athlete, 'total_coachs': total_coachs, 'last_athletes': last_athlete,
                   'total_athlete_gender_man': total_athlete_gender_man,
                   'total_athlete_gender_woman': total_athlete_gender_woman,
                   'total_athlate_last_month': total_athlate_last_month,
                   'total_judge': total_judge, 'total_user': total_user,
                   # 'total_notifications_refere': total_notifications_refere,
                   # 'total_notifications_coach': total_notifications_coach,
                   # 'total_notifications_clup': total_notifications_clup,
                   # 'notifications_tatal': notifications_tatal

                   })


def City_athlete_cout(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            athletecout = Athlete.objects.filter(communication__city__name__icontains=request.POST.get('city')).count()
            coachcout = Coach.objects.filter(communication__city__name__icontains=request.POST.get('city')).count()
            refereecout = Judge.objects.filter(communication__city__name__icontains=request.POST.get('city')).count()
            sportsClub = SportsClub.objects.filter(
                communication__city__name__icontains=request.POST.get('city')).count()
            data = {
                'athlete': athletecout,
                'coach': coachcout,
                'referee': refereecout,
                'sportsClub': sportsClub

            }
            return JsonResponse(data)
        except Level.DoesNotExist:
            return JsonResponse({'status': 'Fail'})

    else:
        return JsonResponse({'status': 'Fail'})
#
#


@login_required
def activeGroup(request, pk):
    userActive = ActiveGroup.objects.get(user=request.user)
    group = Group.objects.get(pk=pk)
    userActive.group = group
    userActive.save()

    if group.name == "Admin":
        return redirect('sbs:admin')
    elif group.name == "Antrenor":
        return redirect('sbs:antrenor')
    elif group.name == 'Hakem':
        return redirect('sbs:hakem', )
    elif group.name == 'KulupUye':
        return redirect('sbs:kulup-uyesi')
    elif group.name == 'Sporcu':
        return redirect('sbs:sporcu')
    elif group.name == 'Yonetim':
        return redirect('sbs:federasyon')
    else:
        return {}
