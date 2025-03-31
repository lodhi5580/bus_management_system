from django.contrib import admin
from .models import Bus, Route, Ticket,RouteBusMap

admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Ticket)
admin.site.register(RouteBusMap)
