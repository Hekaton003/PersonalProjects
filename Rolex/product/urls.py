from django.urls import path
from .views import (
    ProductListView,
    about_page,
    location_page,
    contact_page,
    tennis_page,
    golf_page,
    yacht_page,
    moto_page,
    cinema_page,
    music_page,
    architecture_page)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('about/', about_page, name='about'),
    path('location/', location_page, name='location'),
    path('contact/', contact_page, name='contact'),
    path('tennis/', tennis_page, name='tennis'),
    path('golf/',golf_page, name='golf'),
    path('yacht/',yacht_page, name='yacht'),
    path('moto/',moto_page, name='moto'),
    path('music/',music_page, name='music'),
    path('architecture/',architecture_page, name='architecture'),
    path('cinema/',cinema_page, name='cinema'),
]
