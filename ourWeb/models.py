# -*- encoding: utf-8 -*-
from datetime import date
# Django
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_delete,post_save
from django.dispatch.dispatcher import receiver

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
    date = models.DateField('Fecha en que se realizó el pago', null=True)

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
        if self.status == Order.IN_PROCESS:
            self.total = self.get_total()
            self.save()

    def get_products(self):
        return ProdOrder.objects.filter(order=self)

class ProdOrder(models.Model):

    prod = models.ForeignKey("ourAdmin.Prod",verbose_name='Producto')
    order = models.ForeignKey(Order)
    qty = models.PositiveIntegerField("Cantidad",default=1)

    class Meta:
        unique_together = (('prod','order'),)

    def get_total(self):
        return (self.qty * self.prod.get_TPrice())

    def get_subtotal(self):
        if self.order.status == Order.IN_PROCESS:
            return self.prod.price * self.qty
        else:
            return self.prod.get_price(self.order.date) * self.qty

    def get_taxtotal(self):
        if self.order.status == Order.IN_PROCESS:
            return self.prod.get_tax() * self.qty
        else:
            return self.prod.get_tax(self.order.date) * self.qty      

    def get_total_amount(self):
        if self.order.status == Order.IN_PROCESS:
            return self.prod.get_total() * self.qty
        else:
            return self.prod.get_total(self.order.date) * self.qty

@receiver(post_save, sender=ProdOrder)
def prodOrder_post_save(sender, instance, created, **kwargs):
    if instance.qty == 0:
        instance.delete()
    else:
        instance.order.update_total()
            
class Payment(models.Model):
    order = models.ForeignKey(Order, unique=True,verbose_name='Orden')
    paymentUser = models.ForeignKey("ourAuth.PaymentUser", verbose_name="Medio de pago")
    date = models.DateField('Fecha',auto_now_add=True)
