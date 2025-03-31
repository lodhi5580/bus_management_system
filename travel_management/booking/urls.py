from django.urls import path
from .views import *

urlpatterns = [
    path("", view=home, name="home"),
    path("signup",view=sign_up,name="signup"),
    path("login/", view=user_login, name="user_login"),
    path("allroutes/", view=route_list, name="all_routes"),
    path("busroute/<str:route_id>", view=buses_on_route, name="bus_list"),
    path("book/<str:route_id>", view=book_ticket, name="book"),
    path("logout",view=user_logout,name="logout"),
    path("user_tickets",view=user_tickets,name="user_tickets"),
]
