import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from gestion.models import (
    Socio, PerfilSocio, Credencial,
    Entrenador, PerfilEntrenador, PlanCuota,
    Pago, Actividad, Reserva, Especialidad
)


class Command(BaseCommand):
    help = 'Genera diez registros de cada modelo usando Faker'

    def handle(self, *args, **options):
        fake = Faker('es_ES')

        especialidades = []
        for i in range(10):
            especialidades.append(
                Especialidad.objects.create(
                    nombre=f'{fake.unique.job()} {i}',
                    descripcion=fake.text(max_nb_chars=100),
                    nivel=random.randint(1, 5),
                    codigo=f'fitness-{fake.unique.slug()}-{i}',
                    activa=True,
                )
            )

        entrenadores = []
        for i in range(10):
            entrenador = Entrenador.objects.create(
                nombre=fake.first_name(),
                apellidos=fake.last_name() + ' ' + fake.last_name(),
                email=fake.unique.email(),
                telefono=fake.phone_number()[:15],
                fecha_contratacion=fake.date_between(
                    start_date='-5y', end_date='today'
                ),
            )
            entrenador.especialidades.add(
                random.choice(especialidades)
            )
            PerfilEntrenador.objects.create(
                entrenador=entrenador,
                biografia=fake.text(max_nb_chars=150),
                certificacion=fake.job()[:100],
                fecha_nacimiento=fake.date_of_birth(
                    minimum_age=22, maximum_age=60
                ),
                tarifa_hora=random.randint(15, 50),
                experiencia_anos=random.randint(0, 25),
            )
            entrenadores.append(entrenador)

        planes = []
        for i in range(10):
            planes.append(
                PlanCuota.objects.create(
                    nombre=f'Plan {fake.unique.word()} {i}',
                    descripcion=fake.text(max_nb_chars=100),
                    precio=random.randint(15, 100),
                    duracion_dias=random.choice([7, 30, 90, 365]),
                    activa=True,
                )
            )

        actividades = []
        for i in range(10):
            actividades.append(
                Actividad.objects.create(
                    nombre=f'Actividad {fake.unique.word()} {i}',
                    descripcion=fake.text(max_nb_chars=100),
                    entrenador=random.choice(entrenadores),
                    aforo=random.randint(5, 30),
                    duracion_minutos=random.choice([30, 45, 60, 90]),
                    sala=f'Sala {random.randint(1, 5)}',
                    activa=True,
                )
            )

        socios = []
        for i in range(10):
            socio = Socio.objects.create(
                nombre=fake.first_name(),
                apellidos=fake.last_name() + ' ' + fake.last_name(),
                email=fake.unique.email(),
                telefono=fake.phone_number()[:15],
            )
            PerfilSocio.objects.create(
                socio=socio,
                fecha_nacimiento=fake.date_of_birth(
                    minimum_age=18, maximum_age=75
                ),
                direccion=fake.address()[:150],
                contacto_emergencia=fake.phone_number()[:100],
                observaciones=fake.text(max_nb_chars=100),
            )
            Credencial.objects.create(
                socio=socio,
                codigo=f'CR-{fake.unique.bothify(text="????-####")}',
            )
            socios.append(socio)

        for i in range(10):
            socio = random.choice(socios)
            plan = random.choice(planes)
            Pago.objects.create(
                socio=socio,
                plan=plan,
                importe=plan.precio,
                metodo=random.choice(['EF', 'TA', 'TR']),
                referencia=fake.uuid4(),
                pagado=random.choice([True, False]),
            )

            Reserva.objects.create(
                socio=socio,
                actividad=random.choice(actividades),
                fecha_reserva=timezone.now() + timedelta(days=i + 1),
                estado=random.choice(['P', 'C', 'A']),
                asistio=random.choice([True, False]),
                observaciones=fake.text(max_nb_chars=100),
            )

        self.stdout.write(
            self.style.SUCCESS(
                'Se han creado 10 registros de cada uno de los 10 modelos.'
            )
        )