from django.contrib import admin
from .models import MorningJournal, EveningJournal

from django_summernote.admin import SummernoteModelAdmin

class MorningJournalAdmin(SummernoteModelAdmin):
    list_display = ('title', 'mood', 'start_time', 'created_on','author')
    list_filter = ('mood', 'author')
    summernote_fields = ('q1a','q1b','q1c','q2a','q2b','q2c')
    readonly_fields = ('created_on',)

admin.site.register(MorningJournal, MorningJournalAdmin)

class EveningJournalAdmin(SummernoteModelAdmin):
    list_display = ('title', 'mood', 'start_time', 'created_on','author')
    list_filter = ('mood', 'author')
    summernote_fields = ('q3a','q3b','q3c','q4a','q4b','q4c')
    readonly_fields = ('created_on',)

admin.site.register(EveningJournal, EveningJournalAdmin)