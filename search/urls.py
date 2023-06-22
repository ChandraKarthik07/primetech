from django.urls import path
from .views import search_view,fill_models_from_csv

urlpatterns = [
    path('search/', search_view, name='search'),
    path('fill_models/', fill_models_from_csv, name='fill'),

]
