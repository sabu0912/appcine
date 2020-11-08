from django.db import models
import os
from uuid import uuid4

def image_rename(path):
    def wrapper(instance, filename):
        #descarga.jpg -> ['descarga', 'jpg']
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = f'{instance.pk}.{ext}'
        else:
            filename = f'{uuid4().hex}.{ext}'
        return os.path.join(path, filename) #'picture/author/nombre.ext'
    return wrapper

# Create your models here.

class Tipo_rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    roles = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = 'Tipo_rol'
        verbose_name_plural = 'Tipo_roles'
        ordering = ['roles']

    def _str_(self):
        return f'{self.roles}'

class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=200, blank=False, null=False)
    apellidos = models.CharField(max_length=220, blank=False, null=False)
    dni = models.CharField(max_length=8, blank=False, null=False)
    telefono = models.CharField(max_length=9, blank=False, null=False)
    direccion = models.TextField(blank=False, null=False)
    id_rol  = models.ManyToManyField(Tipo_rol)
    avatar = models.ImageField(upload_to=image_rename('picture/author'), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['nombres']

    def _str_(self):
        return f'{self.nombres} {self.apellidos}'

    def tipo_roles(self):
        return ','.join([str(p) for p in self.id_rol.all()])

class Sede(models.Model):
    id_sede = models.AutoField(primary_key=True)
    sede = models.CharField(max_length=200, blank=False, null=False)
    direccion = models.CharField(max_length=200, blank=False, null=False)
    distrito =models.CharField(max_length=200, blank=False, null=False)
    pais = models.CharField(max_length=200, blank=False, null=False)
    estado_sede = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'
        ordering = ['sede']

    def _str_(self):
        return f'{self.sede}'


class Pelicula(models.Model):
    id_pelicula = models.AutoField(primary_key=True)
    pelicula = models.CharField(max_length=200, blank=False, null=False)
    genero = models.CharField(max_length=200, blank=False, null=False)
    fecha_estreno = models.DateField(auto_now=False,blank=False, null=False)
    clase = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        verbose_name = 'Pelicula'
        verbose_name_plural = 'Pelicula'
        ordering = ['pelicula']

    def _str_(self):
        return f'{self.pelicula}'

class Sala(models.Model):
    id_sala = models.AutoField(primary_key=True)
    id_sede = models.ManyToManyField(Sede)
    sala = models.CharField(max_length=200, blank=False, null=False)
    stock_butacas = models.IntegerField(blank=False, null=False)
    estado_sala = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        ordering = ['sala']

    def _str_(self):
        return f'{self.sala}'

    def peliculas(self):
        return ','.join([str(p) for p in self.id_pelicula.all()])


class Agenda(models.Model):
    id_agenda = models.AutoField(primary_key=True)
    id_sala = models.ManyToManyField(Sala)
    id_pelicula = models.ManyToManyField(Pelicula)
    fecha_agenda = models.DateField(auto_now=False,blank=False, null=False)
    hora_inicio = models.TimeField(blank=False, null=False)
    hora_fin = models.TimeField(blank=False, null=False)
    saldo_butacas = models.IntegerField(blank=False, null=False)

    class Meta:
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agendas'
        ordering = ['agenda']

    def _str_(self):
        return f'{self.fecha_agenda}'

    def salas(self):
        return ','.join([str(p) for p in self.id_sala.all()])

    def peliculas(self):
        return ','.join([str(p) for p in self.id_pelicula.all()])

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    id_cliente = models.ManyToManyField(Persona)
    id_agenda = models.ManyToManyField(Agenda)
    estado_reserva = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['reserva']

    def _str_(self):
        return f'{self.estado_reserva}'

    def clientes(self):
        return ','.join([str(p) for p in self.id_cliente.all()])

    def agendas(self):
        return ','.join([str(p) for p in self.id_agenda.all()])