from django.db import models


class Socio(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    actividades = models.ManyToManyField(
        'Actividad',
        through='Reserva',
        through_fields=('socio', 'actividad'),
        related_name='socios'
    )

    planes_historicos = models.ManyToManyField(
        'PlanCuota',
        through='Pago',
        through_fields=('socio', 'plan'),
        related_name='socios'
    )

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class PerfilSocio(models.Model):
    socio = models.OneToOneField(
        Socio, on_delete=models.CASCADE,
        related_name='perfil'
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=150)
    contacto_emergencia = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.socio}"


class Credencial(models.Model):
    socio = models.OneToOneField(
        Socio, on_delete=models.CASCADE,
        related_name='credencial'
    )
    codigo = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    tipo = models.CharField(max_length=30, default='Socio')

    def __str__(self):
        return self.codigo


class Entrenador(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    fecha_contratacion = models.DateField()
    activo = models.BooleanField(default=True)

    especialidades = models.ManyToManyField(
        'Especialidad',
        related_name='entrenadores'
    )

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class PerfilEntrenador(models.Model):
    entrenador = models.OneToOneField(
        Entrenador, on_delete=models.CASCADE,
        related_name='perfil'
    )
    biografia = models.TextField()
    certificacion = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    tarifa_hora = models.DecimalField(
        max_digits=7, decimal_places=2
    )
    experiencia_anos = models.IntegerField(default=0)

    def __str__(self):
        return f"Perfil de {self.entrenador}"


class PlanCuota(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    duracion_dias = models.PositiveIntegerField(default=30)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Pago(models.Model):
    METODOS = [
        ('EF', 'Efectivo'),
        ('TA', 'Tarjeta'),
        ('TR', 'Transferencia'),
    ]

    socio = models.ForeignKey(
        Socio, on_delete=models.CASCADE,
        related_name='pagos'
    )
    plan = models.ForeignKey(
        PlanCuota, on_delete=models.PROTECT,
        related_name='pagos'
    )
    importe = models.DecimalField(max_digits=7, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo = models.CharField(max_length=2, choices=METODOS)
    referencia = models.CharField(max_length=50, blank=True)
    pagado = models.BooleanField(default=True)

    def __str__(self):
        return f"Pago de {self.socio}: {self.importe} €"


class Actividad(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField()
    entrenador = models.ForeignKey(
        Entrenador, on_delete=models.PROTECT,
        related_name='actividades'
    )
    aforo = models.PositiveIntegerField(default=15)
    duracion_minutos = models.PositiveIntegerField(default=60)
    sala = models.CharField(max_length=30)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    ESTADOS = [
        ('P', 'Pendiente'),
        ('C', 'Confirmada'),
        ('A', 'Anulada'),
    ]

    socio = models.ForeignKey(
        Socio, on_delete=models.CASCADE,
        related_name='reservas'
    )
    actividad = models.ForeignKey(
        Actividad, on_delete=models.CASCADE,
        related_name='reservas'
    )
    fecha_reserva = models.DateTimeField()
    estado = models.CharField(
        max_length=1, choices=ESTADOS, default='P'
    )
    asistio = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['socio', 'actividad', 'fecha_reserva'],
                name='reserva_unica_por_fecha'
            )
        ]

    def __str__(self):
        return f"{self.socio} - {self.actividad}"


class Especialidad(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField()
    nivel = models.PositiveIntegerField(default=1)
    codigo = models.SlugField(max_length=70, unique=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre