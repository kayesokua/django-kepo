from . import views
from django.urls import include, path

urlpatterns = [
    path("", views.PostList.as_view(), name="feed"),
    path('<str:author>/', views.post_by_user, name='post_by_user'),
    path("<str:author>/create/", views.post_create, name="post_create"),
    path("<str:author>/<slug:slug>/", views.post_detail , name="post_detail"),
    path("<str:author>/<slug:slug>/update", views.post_update, name="post_update"),
    path("<str:author>/<slug:slug>/delete", views.post_delete, name="post_delete"),
    path('<str:author>/<slug:slug>/comment/<int:comment_pk>/delete', views.comment_delete, name='comment_delete'),

]