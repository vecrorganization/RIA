# -*- encoding: utf-8 -*-

from datetime import date
# Django
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Table(models.Model):
    TAX = "T"
    CATEGORY = "CA"
    COUNTRY = "CO"
    CLASS = "CL"

    TYPE_CHOICES = (
        (TAX, 'Tax'),
        (CATEGORY, 'Category'),
        (COUNTRY, 'Country'),
        (CLASS, 'Class')
    )

    desc = models.CharField('Descripción',max_length=40)
    type = models.CharField('Tipo', max_length=2,choices=TYPE_CHOICES)
    refer = models.IntegerField('Referencia',null=True,blank=True)
    value1 = models.DecimalField("Valor 1",decimal_places=3,max_digits=9,null=True,blank=True)
    value2 = models.DecimalField("Valor 2",decimal_places=3,max_digits=9,null=True,blank=True)
    modifier = models.ForeignKey(User)
    createDate = models.DateTimeField("Fecha de creación",auto_now_add=True,null=True,blank=True)
    modifyDate = models.DateTimeField("Fecha de modificación",null=True,blank=True)

    class Meta:
        ordering = ['type']

    def __str__(self):
        return self.get_type_display() + ": " + self.desc


class Seller(models.Model):
    
    eMail = models.EmailField(max_length=254,primary_key=True)
    company = models.CharField('Compañía',max_length=100, null=True)
    legalNum = models.CharField('Num. Legal',max_length=25,null=True)
    contactName = models.CharField('Nombre de contacto',max_length=100)
    contactPhone = models.CharField('Telf. de contacto',max_length=25)
    contactMail = models.EmailField('Mail de contacto',max_length=50)
    country = models.ForeignKey(Table)
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
    desc  = models.CharField('Descripción', max_length=100)
    price = models.DecimalField('Precio',max_digits=12,
                                  decimal_places=3, validators=[MinValueValidator(0.0)])
    category = models.ForeignKey(Table, related_name='category')
    clase = models.ForeignKey(Table, related_name='clase')
    width = models.DecimalField('Anchura',max_digits=9,decimal_places=3, 
                                    validators=[MinValueValidator(0.0)],null=True,blank=True)
    length = models.DecimalField('Longitud',max_digits=9,decimal_places=3, 
                                    validators=[MinValueValidator(0.0)],null=True,blank=True)
    height = models.DecimalField('Altura',max_digits=9,decimal_places=3, 
                                    validators=[MinValueValidator(0.0)],null=True,blank=True)
    tax1 = models.ForeignKey(Table, related_name='tax1')
    tax2 = models.ForeignKey(Table, related_name='tax2')
    seller = models.ForeignKey(Seller)
    image_1 = models.ImageField(upload_to='preguntar/')
    image_2 = models.ImageField(null=True,blank=True,upload_to='preguntar/')
    image_3 = models.ImageField(null=True,blank=True,upload_to='preguntar/')
    image_4 = models.ImageField(null=True,blank=True,upload_to='preguntar/')
    image_5 = models.ImageField(null=True,blank=True,upload_to='preguntar/')
    modifier = models.ForeignKey(User, related_name='prod_modifier')
    createDate = models.DateField('Fecha de creación',auto_now_add=True)
    modifyDate = models.DateField('Fecha de modificación', null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.modifyDate = date.today()
        return super(Prod, self).save(*args, **kwargs)

class MPayment(models.Model):
    cardNumber = models.DecimalField('Numero tarjeta', max_digits=20, decimal_places=0, validators=[MinValueValidator(0.0)], primary_key=True)
    cardType = models.CharField('Tipo tarjeta', max_length=25)
    cardCountry = models.CharField('País', max_length=25, null=True)
    cardName = models.CharField('Nombre tarjeta', max_length=25)
    dueDateM = models.CharField(max_length=2)
    dueDateY = models.CharField(max_length=4)
    cardCod = models.PositiveSmallIntegerField()


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


class Adress(models.Model):
    State = models.CharField('Descripción',max_length=50)
    Address1 = models.CharField('Descripción',max_length=254)
    Address2 = models.CharField('Descripción',max_length=254)
    Telephone = models.CharField('Descripción',max_length=50)

class AddressUser(models.Model):
    User = models.ForeignKey(User)
    Address = models.ForeignKey(Adress)
    
    class Meta:
        unique_together = (('User','Address'),)



class Order(models.Model):
    Address = models.ForeignKey(Adress)