from django.urls import path
from .views import  IndexPageView, indexView, addVehiculo, registro_view, login_view, listar_vehiculo, logout_view

urlpatterns=[
    path('', IndexPageView.as_view(), name='index'), # esto es con clases. Se usa el metodo as_view()
    path('',indexView, name='index'),
    path('add/',addVehiculo, name='addform'),
    path('registro/', registro_view, name= "registro"),
    path('login/', login_view, name= "login"),
    path('listar/', listar_vehiculo, name= "listar"),
    path('logout/', logout_view, name= "logout"),
]