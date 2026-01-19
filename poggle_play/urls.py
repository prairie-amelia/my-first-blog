from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_board, name='new_board'),
    path('<str:boardString>/',views.show_board, name = "show_board"),
    path('<str:boardString>/<str:wordString>/',views.enter_word, name = "enter_word"),
]