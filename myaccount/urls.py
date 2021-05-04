from django.urls import path
from myaccount import views
app_name = 'myaccount'

urlpatterns = [
      path('', views.account_settings, name='account_settings'),
      path('update/', views.account_update, name='account_update'),
      path('password/update', views.password_update, name='password_update'),
      path('sign_in/', views.sign_in, name="sign_in")
]