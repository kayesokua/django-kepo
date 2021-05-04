from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db import IntegrityError

from django.utils import timezone
from django.utils.safestring import mark_safe

from django.views import generic

import calendar
import random

from datetime import datetime, timedelta, time, date

from .utils import Calendar
from .forms import MorningJournalForm, EveningJournalForm
from .models import MorningJournal, EveningJournal

import os.path
BASE = os.path.dirname(os.path.abspath(__file__))

def journal_count(request):
    today = datetime.now().date()
    #Total Journal Count for a month
    morning_count = MorningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month).count()
    evening_count = EveningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month).count()
    post_count_total = int(morning_count) + int(evening_count)
    return post_count_total

@login_required
def journal_today(request):
    today = datetime.now().date()
    # Filter objects that ranges from today until the next day
    morningjournals = MorningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month,start_time__day=today.day)
    eveningjournals = EveningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month,start_time__day=today.day)
    
    #randomises headline
    questions = open(os.path.join(BASE, "data/questions.txt"))
    data = questions.read().splitlines()
    headline = random.choice(data)

    #Total Journal Count for a month
    morning_count = MorningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month).count()
    evening_count = EveningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month).count()
    post_count_total = int(morning_count) + int(evening_count)

    return render(request, 'myjournal/today.html', {'morningjournals':morningjournals,'eveningjournals':eveningjournals,'today':today,'headline':headline,'post_count_total':post_count_total})

@login_required
def morning_create(request):
    today = datetime.now().date()
    today_datetimelocal = datetime.now().strftime("%Y-%m-%dT%H:%M")
    last7days = datetime.now() - timedelta(7)
    today_datetimelocal_min = last7days.strftime("%Y-%m-%dT%H:%M")

    if request.method == 'GET':
        return render(request, 'myjournal/morning_create.html', {'form':MorningJournalForm(),'today':today,'today_datetimelocal':today_datetimelocal,'today_datetimelocal_min':today_datetimelocal_min})
    else:
        if MorningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month,start_time__day=today.day).exists():
            return render(request, 'myjournal/morning_create.html', {'form':MorningJournalForm(), 'error':'You already made an entry today!','today':today,'today_datetimelocal':today_datetimelocal,'today_datetimelocal_min':today_datetimelocal_min})
        else:
            try:
                form = MorningJournalForm(request.POST)
                new_morningjournal = form.save(commit=False)
                #autopopulates the author model fied with signed in user
                new_morningjournal.author = request.user
                new_morningjournal.save()
                return redirect('myjournal:journal_today')
            except ValueError:
                return render(request, 'myjournal/morning_create.html', {'form':MorningJournalForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def morning_update(request, morningjournal_pk):
    morningjournal = get_object_or_404(MorningJournal, pk=morningjournal_pk, author=request.user)
    morningjournal.start_time = morningjournal.start_time.strftime("%Y-%m-%dT%H:%M")
    if request.method == 'GET':
        form = MorningJournalForm(instance=morningjournal)
        return render(request, 'myjournal/morning_update.html', {'morningjournal':morningjournal, 'form':form})
    else:
        try:
            form = MorningJournalForm(request.POST, instance=morningjournal)
            form.save()
            today = datetime.now().date()
            morningjournals = MorningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month,start_time__day=today.day)
            eveningjournals = EveningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month,start_time__day=today.day)
            return render(request, 'myjournal/today.html', {'morningjournal':morningjournal, 'form':form, 'error':'','info':'successfully updated!', 'morningjournals':morningjournals,'eveningjournals':eveningjournals,'today':today})
        except ValueError:
            return render(request, 'myjournal/morning_update.html', {'morningjournal':morningjournal, 'form':form, 'error':'Bad info passed in. Try again?'})

@login_required
def morning_delete(request, morningjournal_pk):
    morningjournal = get_object_or_404(MorningJournal, pk=morningjournal_pk, author=request.user)
    if request.method == 'POST':
        morningjournal.delete()
        return render(request, 'myjournal/today.html', {'morningjournal':morningjournal, 'error':'The post has been deleted'})

@login_required
def evening_create(request):
    today = datetime.now().date()
    today_datetimelocal = datetime.now().strftime("%Y-%m-%dT%H:%M")
    last7days = datetime.now() - timedelta(7)
    today_datetimelocal_min = last7days.strftime("%Y-%m-%dT%H:%M")

    if request.method == 'GET':
        return render(request, 'myjournal/evening_create.html', {'form':EveningJournalForm(),'today':today,'today_datetimelocal':today_datetimelocal,'today_datetimelocal_min':today_datetimelocal_min})
    else:
        if EveningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month,start_time__day=today.day).exists():
            return render(request, 'myjournal/evening_create.html', {'form':EveningJournalForm(), 'error':'You already made an entry today!','today':today,'today_datetimelocal':today_datetimelocal,'today_datetimelocal_min':today_datetimelocal_min})
        else:
            try:
                form = EveningJournalForm(request.POST)
                new_eveningjournal = form.save(commit=False)

                #autopopulates the author model fied with signed in user
                new_eveningjournal.author = request.user
                new_eveningjournal.save()
                return redirect('myjournal:journal_today')
            except ValueError:
                return render(request, 'myjournal/evening_create.html', {'form':EveningJournalForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def evening_update(request, eveningjournal_pk):
    eveningjournal = get_object_or_404(EveningJournal, pk=eveningjournal_pk, author=request.user)
    eveningjournal.start_time = eveningjournal.start_time.strftime("%Y-%m-%dT%H:%M")
    if request.method == 'GET':
        form = EveningJournalForm(instance=eveningjournal)
        return render(request, 'myjournal/evening_update.html', {'eveningjournal':eveningjournal, 'form':form})
    else:
        try:
            form = EveningJournalForm(request.POST, instance=eveningjournal)
            form.save()
            today = datetime.now().date()
            morningjournals = MorningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month,start_time__day=today.day)
            eveningjournals = EveningJournal.objects.filter(author=request.user, start_time__year=today.year,start_time__month=today.month,start_time__day=today.day)
            return render(request, 'myjournal/today.html', {'eveningjournal':eveningjournal, 'form':form, 'error':'','info':'successfully updated!', 'morningjournals':morningjournals,'eveningjournals':eveningjournals,'today':today})
        except ValueError:
            return render(request, 'myjournal/evening_update.html', {'eveningjournal':eveningjournal, 'form':form, 'error':'Bad info passed in. Try again?'})

@login_required
def evening_delete(request, eveningjournal_pk):
    eveningjournal = get_object_or_404(EveningJournal, pk=eveningjournal_pk, author=request.user)
    if request.method == 'POST':
        eveningjournal.delete()
        return render(request, 'myjournal/evening_update.html', {'eveningjournal':eveningjournal, 'error':'The post has been deleted'})

class CalendarView(LoginRequiredMixin, generic.ListView):
    model = MorningJournal
    template_name = 'myjournal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        author = self.request.user
        cal = Calendar(d.year, d.month, author)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month