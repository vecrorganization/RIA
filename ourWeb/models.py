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

    def get_subtotal(self):
        prods = ProdOrder.objects.filter(order = self)
        subtotal = 0
        for p in prods:
            subtotal += p.get_subtotal()
        return subtotal


    def get_total(self):
        prods = ProdOrder.objects.filter(order = self)
        total = 0
        for p in prods:
            total += p.get_total()
        return total

    def get_taxtotal(self):
        prods = ProdOrder.objects.filter(order = self)
        taxTotal = 0
        for p in prods:
            taxTotal += p.get_taxtotal()
        return taxTotal        

    def update_total(self):
        self.total = self.get_total()

class ProdOrder(models.Model):

    prod = models.ForeignKey("ourAdmin.Prod",verbose_name='Producto')
    order = models.ForeignKey(Order)
    qty = models.PositiveIntegerField("Cantidad",default=1)

    class Meta:
        unique_together = (('prod','order'),)

    def get_total_amount(self):
        return (self.prod.price + self.prod.get_tax1()) * self.qty

    def get_total(self):
        return (self.qty * self.prod.get_TPrice())

    def get_subtotal(self):
        return (self.qty * self.prod.price)

    def get_taxtotal(self):
        return (self.qty * self.prod.get_tax1())        

class Payment(models.Model):
    order = models.ForeignKey(Order, unique=True,verbose_name='Orden')
    paymentUser = models.ForeignKey("ourAuth.PaymentUser", verbose_name="Medio de pago")
    date = models.DateField('Fecha',auto_now_add=True)
