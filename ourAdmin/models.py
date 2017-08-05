# -*- encoding: utf-8 -*-
from datetime import date
from decimal import Decimal
# Django
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_delete,post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Table(models.Model):
    TAX = "T"
    CATEGORY = "CA"
    COUNTRY = "CO"
    STATE = "ST"
    CLASS = "CL"

    TYPE_CHOICES = (
        (TAX, 'Tax'),
        (CATEGORY, 'Category'),
        (COUNTRY, 'Country'),
        (STATE, 'State'),
        (CLASS, 'Class')
    )

    desc = models.CharField('Descripción',max_length=40)
    type = models.CharField('Tipo', max_length=2,choices=TYPE_CHOICES)
    refer = models.ForeignKey("Table",null=True,blank=True)
    value1 = models.DecimalField("Valor 1",decimal_places=3,max_digits=9,null=True,blank=True)
    value2 = models.DecimalField("Valor 2",decimal_places=3,max_digits=9,null=True,blank=True)
    modifier = models.ForeignKey(User)
    createDate = models.DateTimeField("Fecha de creación",auto_now_add=True,null=True,blank=True)
    modifyDate = models.DateTimeField("Fecha de modificación",null=True,blank=True)

    class Meta:
        ordering = ['type']

    def __str__(self):
        return self.get_type_display() + ": " + self.desc

    def get_desc(self):
        return self.desc        


class Seller(models.Model):
    
    eMail = models.EmailField(max_length=254,primary_key=True)
    company = models.CharField('Compañía',max_length=100, null=True)
    legalNum = models.CharField('Num. Legal',max_length=25,null=True)
    contactName = models.CharField('Nombre de contacto',max_length=100)
    contactPhone = models.CharField('Telf. de contacto',max_length=25)
    contactMail = models.EmailField('Mail de contacto',max_length=50)
    country = models.ForeignKey(Table,verbose_name='País')
    city = models.CharField('Ciudad',max_length=50)
    zipCode = models.CharField('Código postal',max_length=10,null=True)
    address = models.CharField('Dirección',max_length=50)
    modifier = models.ForeignKey(User)
    createDate = models.DateTimeField("Fecha de creación",auto_now_add=True,null=True)
    modifyDate = models.DateTimeField("Fecha de modificación", null=True)

    class Meta:
        ordering = ['country']

    def __str__(self):
        return self.eMail


class Prod(models.Model):

    id = models.CharField(max_length=25, primary_key=True)
    name  = models.CharField('Nombre', max_length=100)
    desc  = models.CharField('Descripción', max_length=250)
    price = models.DecimalField('Precio',max_digits=15,
                                  decimal_places=3, validators=[MinValueValidator(0.0)])
    width = models.DecimalField('Anchura',max_digits=9,decimal_places=3, 
                                    validators=[MinValueValidator(0.0)],null=True,blank=True)
    length = models.DecimalField('Longitud',max_digits=9,decimal_places=3, 
                                    validators=[MinValueValidator(0.0)],null=True,blank=True)
    height = models.DecimalField('Altura',max_digits=9,decimal_places=3, 
                                    validators=[MinValueValidator(0.0)],null=True,blank=True)
    category = models.ForeignKey(Table, related_name='category',verbose_name='Categoría')
    clase = models.ForeignKey(Table, related_name='clase')
    tax1 = models.ForeignKey(Table, related_name='tax1')
    tax2 = models.ForeignKey(Table, related_name='tax2', null=True, blank=True)
    seller = models.ForeignKey(Seller,verbose_name='Vendedor')
    modifier = models.ForeignKey(User, related_name='prod_modifier')
    image_1 = models.ImageField(upload_to='prod/')
    image_2 = models.ImageField(null=True,blank=True,upload_to='prod/')
    image_3 = models.ImageField(null=True,blank=True,upload_to='prod/')
    image_4 = models.ImageField(null=True,blank=True,upload_to='prod/')
    image_5 = models.ImageField(null=True,blank=True,upload_to='prod/')
    createDate = models.DateField('Fecha de creación',auto_now_add=True)
    modifyDate = models.DateField('Fecha de modificación', null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.modifyDate = date.today()

            orig = Prod.objects.get(pk=self.pk)
            if orig.price != self.price:
                super(Prod, self).save(*args, **kwargs)
                from ourWeb.controller import post_update_prod_price
                post_update_prod_price(self)
                ProdPriceRecord.objects.create(prod=self,price=self.price)
                return self 

        return super(Prod, self).save(*args, **kwargs)

    def get_tax_percent(self):
        return self.tax1.value1

    def get_price(self,date=None):
        if date:
            try:
                closest_prod = ProdPriceRecord.objects.filter(prod= self, date__lte = date).order_by('-date')
                return closest_prod[0].price
            except IndexError:
                pass
        return self.price

    def get_tax(self,date=None):
        return round(self.get_price(date) * self.tax1.value1 * Decimal(0.01),3)

    def get_total(self,date=None):
        price = self.get_price(date)
        return price + round(price * self.tax1.value1 * Decimal(0.01),3)

    def get_TPrice(self):
        return self.price + self.get_tax()

    def get_images(self):
        images = []
        if self.image_1:
            images.append(self.image_1)
            if self.image_2:
                images.append(self.image_2)
            if self.image_3:
                images.append(self.image_3)
            if self.image_4:
                images.append(self.image_4)
            if self.image_5:
                images.append(self.image_5)
        return images


@receiver(post_save, sender=Prod)
def prod_post_save(sender, instance, created, **kwargs):
    if created:
        ProdPriceRecord.objects.create(prod = instance,price = instance.price)
        
@receiver(pre_delete, sender=Prod)
def prod_pre_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image_1.delete(False)
    instance.image_2.delete(False)
    instance.image_3.delete(False)
    instance.image_4.delete(False)
    instance.image_5.delete(False)
    
class ProdPriceRecord(models.Model):
    prod  = models.ForeignKey(Prod)
    date = models.DateField('Fecha de modificación',auto_now_add=True)
    price = models.DecimalField('Precio',decimal_places=3,
                                  max_digits=12, validators=[MinValueValidator(0.0)])

class PaymentMethod(models.Model):
    cardNumber = models.DecimalField('Numero tarjeta', max_digits=20, decimal_places=0, validators=[MinValueValidator(0.0)], primary_key=True)
    cardType = models.CharField('Tipo tarjeta', max_length=25)
    cardCountry = models.CharField('País', max_length=25, null=True,blank=True)
    cardName = models.CharField('Nombre tarjeta', max_length=25)
    dueDateM = models.CharField(max_length=2)
    dueDateY = models.CharField(max_length=4)
    cardCod = models.PositiveSmallIntegerField()


class Address(models.Model):
    state = models.ForeignKey(Table,verbose_name='State')
    address1 = models.CharField('Dirección 1',max_length=254)
    address2 = models.CharField('Dirección 2',max_length=254, null=True)
    telephone = models.CharField('Teléfono',max_length=50)
    zipCode = models.CharField('Código postal',max_length=10)

    def __str__(self):
        if self.address2:
            return self.state.get_desc() + ": " + self.address1 + " / " + self.address2
        else:
            return self.state.get_desc() + ": " + self.address1

class HDiscount(models.Model):
    desc = models.CharField( max_length=100)
    dateStart = models.DateField('Fecha de inicio')
    dateFinish = models.DateField('Fecha de finalización')
    porDiscount = models.DecimalField('Porcentaje de descuento',max_digits=6,
                                  decimal_places=2, validators=[MinValueValidator(0.0)], null=True)
    modifier = models.ForeignKey(User)
    createDate = models.DateField('Fecha de creación',auto_now_add=True)
    modifyDate = models.DateField('Fecha de modificación', null=True)


class DDiscount(models.Model):
    #Django no permite claves primarias compuestas

    hd = models.ForeignKey(HDiscount)
    prod = models.ForeignKey(Prod)

    class Meta:
        unique_together = (('hd','prod'),)
