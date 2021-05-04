from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

MOOD = ((0, "Neutral"), (1, "Silly"), (2, "Dreamy"), (3, "Creative"), (4, "Active"))

class MorningJournal(models.Model):
    title = models.CharField(max_length=200)
    q1a = models.CharField(max_length=200,default="")
    q1b = models.CharField(max_length=200,default="")
    q1c = models.CharField(max_length=200,default="")
    q2a = models.CharField(max_length=200,default="")
    q2b = models.CharField(max_length=200,default="")
    q2c = models.CharField(max_length=200,default="")
    mood = models.IntegerField(choices=MOOD, default=0)
    start_time = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="morning_entries")
    
    @property
    def get_absolute_url(self):
        return reverse('month_calendar_detail', kwargs={'pk': self.pk})
        
class EveningJournal(models.Model):
    title = models.CharField(max_length=200)
    q3a = models.CharField(max_length=200,default="")
    q3b = models.CharField(max_length=200,default="")
    q3c = models.CharField(max_length=200,default="")
    q4a = models.CharField(max_length=200,default="")
    q4b = models.CharField(max_length=200,default="")
    q4c = models.CharField(max_length=200,default="")
    mood = models.IntegerField(choices=MOOD, default=0)
    start_time = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="evening_entries")

    @property
    def get_absolute_url(self):
        url = reverse("myjournal:evening_update", kwargs={"pk": self.pk})
        return f'<a href="{url}"> {self.title}</a>'
