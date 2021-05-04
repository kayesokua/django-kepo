from django.urls import path
from django.conf.urls import url

from myjournal import views

app_name = 'myjournal'
urlpatterns = [
    path('today/', views.journal_today, name='journal_today'),
    path('today/morning/create', views.morning_create, name='morning_create'),
    path('morning/<int:morningjournal_pk>/view', views.morning_update, name='morning_update'),
    path('morning/<int:morningjournal_pk>/delete', views.morning_delete, name='morning_delete'),
    path('today/evening/create', views.evening_create, name='evening_create'),
    path('evening/<int:eveningjournal_pk>/view', views.evening_update, name='evening_update'),
    path('evening/<int:eveningjournal_pk>/delete', views.evening_delete, name='evening_delete'),
    path('month/', views.CalendarView.as_view(), name='calendar'),
    path('month/morning/<int:morningjournal_pk>/view', views.morning_update, name='morning_update'),
    path('month/evening/<int:eveningjournal_pk>/view', views.evening_update, name='evening_update'),

]