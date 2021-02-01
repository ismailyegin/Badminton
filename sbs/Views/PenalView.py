from itertools import combinations

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from sbs.Forms.CompetitionForm import CompetitionForm
from sbs.Forms.CompetitionSearchForm import CompetitionSearchForm
from django.db.models import Q
from sbs.models import SportClubUser, SportsClub, Competition, Athlete, CompAthlete, Weight
from sbs.models.SimpleCategory import SimpleCategory
from sbs.models.EnumFields import EnumFields
from sbs.services import general_methods
from sbs.Forms.SimplecategoryForm import SimplecategoryForm
from sbs.models.Person import Person
from sbs.Forms.UserSearchForm import UserSearchForm
from sbs.Forms.SearchClupForm import SearchClupForm

from datetime import date, datetime
from django.utils import timezone

from unicode_tr import unicode_tr


@login_required
def return_penal_athlete(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserSearchForm()
    sportclup = SearchClupForm(request.POST, request.FILES or None)
    data = []
    if request.method == 'POST':
        sportsclup = request.POST.get('sportsClub')
        coach = request.POST.get('coach')
        firstName = unicode_tr(request.POST.get('first_name')).upper()
        lastName = unicode_tr(request.POST.get('last_name')).upper()
        tcno = request.POST.get('tc')
        email = request.POST.get('email')
        if not (firstName or lastName or email or sportsclup or coach or tcno):
            test = Athlete.objects.exclude(person__penal__penal=None)
            for item in test:
                for penals in item.person.penal.all():
                    beka = {
                        'name': item.user.get_full_name(),
                        'penal': penals.penal,
                        'document': penals.file,
                    }
                    data.append(beka)
        elif firstName or lastName or email or sportsclup or coach or tcno:

            query = Q()

            clubsPk = []

            clubs = SportsClub.objects.filter(name=request.POST.get('sportsClub'))

            for club in clubs:
                clubsPk.append(club.pk)

            if firstName:
                query &= Q(user__first_name__icontains=firstName)

            if tcno:
                query &= Q(person__tc__icontains=tcno)

            if lastName:
                query &= Q(user__last_name__icontains=lastName)

            if email:
                query &= Q(user__email__icontains=email)

            if sportsclup:
                query &= Q(licenses__sportsClub__in=clubsPk)
            if coach:
                query &= Q(licenses__coach=coach)
            test = Athlete.objects.exclude(person__penal__penal=None).filter(query).distinct()
            for item in test:
                for penals in item.person.penal.all():
                    beka = {
                        'name': item.user.get_full_name(),
                        'penal': penals.penal,
                        'document': penals.file,
                    }
                    data.append(beka)
    return render(request, 'Ceza/ceza-Listesi-Sporcu.html', {'activity': data,
                                                             'user_form': user_form,
                                                             'Sportclup': sportclup})
