# -*- encoding: utf-8 -*-
from datetime import date
# Django
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Order(models.Model):
    IN_PROCESS = "P"
    COMPLETED = "F"
    CANCELED = "C"

    STATUS_CHOICES = (
        (IN_PROCESS, 'En proceso'),
        (COMPLETED, 'Completada'),
        (CANCELED, 'Cancelada')
    )

    user = models.ForeignKey(User)
    address = models.ForeignKey("ourAdmin.Address",verbose_name='Dirección',null=True)
    total = models.DecimalField(max_digits=12,decimal_places=3,validators=[MinValueValidator(0.0)],default=0.0)
    status = models.CharField('Estatus',max_length=1,choices=STATUS_CHOICES,default=IN_PROCESS)

class ProdOrder(models.Model):

    prod = models.ForeignKey("ourAdmin.Prod",verbose_name='Producto')
    order = models.ForeignKey(Order)
    qty = models.PositiveIntegerField("Cantidad",default=1)

    class Meta:
        unique_together = (('prod','order'),)

class Payment(models.Model):
    order = models.ForeignKey(Order, unique=True,verbose_name='Orden')
    paymentUser = models.ForeignKey("ourAuth.PaymentUser", verbose_name="Medio de pago")
    date = models.DateField('Fecha',auto_now_add=True)
