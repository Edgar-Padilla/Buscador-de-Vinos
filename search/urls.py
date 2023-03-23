from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name="home"),
    path('search', views.search, name="search"),
    #path('avanzada', views.avanzada, name="avanzada"),
    #path('searchAvanzada', views.search, name="searchAvanzada")
]
