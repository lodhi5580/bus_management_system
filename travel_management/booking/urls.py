from django.urls import path
from .views import *

urlpatterns = [
    path("", view=home, name="home"),
    path("allroutes/", view=route_list, name="all_routes"),
    path("busroute/<route_id:str>", view=buses_on_route, name="bus_list"),
    path("book/<route_id:str>", view=buses_on_route, name="book"),
]
