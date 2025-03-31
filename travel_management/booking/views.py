from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from travel_management.booking.models import Route, RouteBusMap, Ticket
from .forms import SignUpForm, LoginForm
from travel_utils.utilities import calculate_route_fare


def home(request):
    return render(request, "booking/home.html")


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(user, password=password)
            login(request, user)
            return redirect("home")

    else:
        form = SignUpForm()

    return render(request, "booking/signup.html", context={"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                remember_me = form.cleaned_data.get("remember_me")
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect("home")
    else:
        form = LoginForm()
    return render(request, "booking/login.html", context={"form": form})


def route_list(request):
    all_routes = Route.objects.all()
    data = {"data": all_routes}

    return render(request, "booking/all_routes.html", context=data)


def buses_on_route(request, route_id):
    route = Route.objects.filter(id=route_id).first()
    data = {}
    if route:
        all_buses = RouteBusMap.objects.filter(route=route)
        data["data"] = all_buses

    return render(request, "booking/buses_on_route.html", context=data)


@login_required
def book_ticket(request, route_id):
    route_map = RouteBusMap.objects.filter(route=route_id).first()
    data = {"data": route_map}
    if request.method == "POST":
        route_id = request.POST.get("route_id")
        number_of_seats = request.POST.get("number_of_seats", 0)

        route_map = RouteBusMap.objects.filter(route=route_id)
        if route_map:
            seats_booked = route_map.seats_booked(number_of_seats)
            if seats_booked:
                total_price = calculate_route_fare(
                    number_of_seats, route_map.ticket_price
                )
                ticket = Ticket.objects.create(
                    user=request.user, route=route_map, seat_number=1, price=total_price
                )
                return render(
                    request, "booking/ticket_booked.html", context={"data": ticket}
                )
            return render(
                request, "booking/not_enough_seats.html", context={"data": route_map}
            )

    return render(request, "booking/book_ticket.html", context=data)
