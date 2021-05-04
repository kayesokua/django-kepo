from django.forms import ModelForm, DateInput
from .models import MorningJournal, EveningJournal

class MorningJournalForm(ModelForm):

  class Meta:
    model = MorningJournal
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = {'title','q1a','q1b','q1c','q2a','q2b','q2c','mood','start_time'}

  def __init__(self, *args, **kwargs):
    super(MorningJournalForm, self).__init__(*args, **kwargs)
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['q1a'].required = False
    self.fields['q1b'].required = False
    self.fields['q1c'].required = False
    self.fields['q2a'].required = False
    self.fields['q2b'].required = False
    self.fields['q2c'].required = False

class EveningJournalForm(ModelForm):

  class Meta:
    model = EveningJournal
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = {'title','q3a','q3b','q3c','q4a','q4b','q4c','mood','start_time'}

  def __init__(self, *args, **kwargs):
    super(EveningJournalForm, self).__init__(*args, **kwargs)
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['q3a'].required = False
    self.fields['q3b'].required = False
    self.fields['q3c'].required = False
    self.fields['q4a'].required = False
    self.fields['q4b'].required = False
    self.fields['q4c'].required = False