from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from gestion.models import (
    Socio, PerfilSocio, Credencial,
    Entrenador, PerfilEntrenador, PlanCuota,
    Pago, Actividad, Reserva, Especialidad
)


class Command(BaseCommand):
    help = 'Crea datos iniciales para el gimnasio'

    def handle(self, *args, **options):
        plan, _ = PlanCuota.objects.get_or_create(
            nombre='Mensual',
            defaults={
                'descripcion': 'Cuota mensual del gimnasio',
                'precio': 30,
                'duracion_dias': 30,
            }
        )

        especialidad, _ = Especialidad.objects.get_or_create(
            codigo='fitness',
            defaults={
                'nombre': 'Fitness',
                'descripcion': 'Entrenamiento general',
                'nivel': 1,
            }
        )

        entrenador, creado = Entrenador.objects.get_or_create(
            email='entrenador@gimnasio.com',
            defaults={
                'nombre': 'Carlos',
                'apellidos': 'García López',
                'telefono': '600123456',
                'fecha_contratacion': timezone.localdate(),
            }
        )

        entrenador.especialidades.add(especialidad)

        if creado:
            PerfilEntrenador.objects.create(
                entrenador=entrenador,
                biografia='Entrenador del gimnasio',
                certificacion='Entrenador personal',
                fecha_nacimiento='1990-05-15',
                tarifa_hora=20,
                experiencia_anos=5,
            )

        actividad, _ = Actividad.objects.get_or_create(
            nombre='Entrenamiento funcional',
            defaults={
                'descripcion': 'Clase de entrenamiento funcional',
                'entrenador': entrenador,
                'aforo': 15,
                'duracion_minutos': 60,
                'sala': 'Sala 1',
            }
        )

        socio, creado = Socio.objects.get_or_create(
            email='socio@gimnasio.com',
            defaults={
                'nombre': 'Ana',
                'apellidos': 'Martínez Pérez',
                'telefono': '611222333',
            }
        )

        if creado:
            PerfilSocio.objects.create(
                socio=socio,
                fecha_nacimiento='2000-01-10',
                direccion='Calle Mayor 10',
                contacto_emergencia='600111222',
                observaciones='Socio de prueba',
            )

            Credencial.objects.create(
                socio=socio,
                codigo='SOCIO-001',
            )

        Pago.objects.get_or_create(
            socio=socio,
            plan=plan,
            defaults={
                'importe': plan.precio,
                'metodo': 'TA',
                'pagado': True,
            }
        )

        Reserva.objects.get_or_create(
            socio=socio,
            actividad=actividad,
            fecha_reserva=timezone.now() + timedelta(days=1),
            defaults={'estado': 'C'},
        )

        self.stdout.write(
            self.style.SUCCESS('Datos iniciales creados correctamente')
        )