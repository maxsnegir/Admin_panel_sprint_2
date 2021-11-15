from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from . import views

urlpatterns = [
    path('movies/', views.Movies.as_view()),
    path('movies/<uuid:pk>/', views.MoviesDetailApi.as_view()),
]