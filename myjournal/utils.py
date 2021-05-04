
from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import MorningJournal, EveningJournal

from django.contrib.auth.models import User

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, user=None):
		self.year = year
		self.month = month
		self.user = user
		super(Calendar, self).__init__()

	#Formats the week to table cell elements
	def formatday(self, day, morningjournals, eveningjournals):
		morningjournals_per_day = morningjournals.filter(start_time__day=day,author=self.user)
		eveningjournals_per_day = eveningjournals.filter(start_time__day=day,author=self.user)
		d = ''
		for morningjournal in morningjournals_per_day:

			#To fix: Get absolute url is not showing properly
			d += f'<li> <a href="morning/{morningjournal.id}/view"> Morning Entry </a> <i class="bi bi-sun"></i></li>'

		for eveningjournal in eveningjournals_per_day:
			
			#To fix: Get absolute url is not showing properly
			d += f'<li> <a href="evening/{eveningjournal.id}/view"> Evening Entry </a> <i class="bi bi-moon"></i></li>'

		current_date = datetime.now().strftime("%d")
		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	#Formats the week to table row elements
	def formatweek(self, theweek, morningjournals, eveningjournals):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, morningjournals, eveningjournals)
		return f'<tr> {week} </tr>'

	#Formats the month to table
	def formatmonth(self, withyear=True):
		morningjournals = MorningJournal.objects.filter(start_time__year=self.year, start_time__month=self.month)
		eveningjournals = EveningJournal.objects.filter(start_time__year=self.year, start_time__month=self.month)
		
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, morningjournals, eveningjournals)}\n'
		return cal