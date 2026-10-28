from django.contrib import admin
from .models import (
    Socio, PerfilSocio, Credencial,
    Entrenador, PerfilEntrenador, PlanCuota,
    Pago, Actividad, Reserva, Especialidad
)

admin.site.register(Socio)
admin.site.register(PerfilSocio)
admin.site.register(Credencial)
admin.site.register(Entrenador)
admin.site.register(PerfilEntrenador)
admin.site.register(PlanCuota)
admin.site.register(Pago)
admin.site.register(Actividad)
admin.site.register(Reserva)
admin.site.register(Especialidad)