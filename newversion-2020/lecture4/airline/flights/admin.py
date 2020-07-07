from django.contrib import admin
from .models import Flight,Airport,Passengers

#If I wanna see more details about Flight:I can specify my settings of displaying and add the setting in a class

class FlightAdmin(admin.ModelAdmin):
    list_display = ("id","origin", "destination","duration")
class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)


admin.site.register(Airport)
admin.site.register(Flight,FlightAdmin)
admin.site.register(Passengers,PassengerAdmin)
