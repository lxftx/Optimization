from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("calculate/", views.calculate, name='Calculate'),
    path("add_values/", views.add_values, name='AddValues'),
]