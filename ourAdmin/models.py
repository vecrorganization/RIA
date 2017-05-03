# -*- encoding: utf-8 -*-

from datetime import date
# Django
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Table(models.Model):
    TAX = "T"
    CATEGORY = "CA"
    COUNTRY = "CO"

    TYPE_CHOICES = (
        (TAX, 'Tax'),
        (CATEGORY, 'Category'),
        (COUNTRY, 'Country')
    )

    desc = models.CharField('Descripción',max_length=40)
    type = models.CharField('Tipo', max_length=2,choices=TYPE_CHOICES)
    refer = models.IntegerField('Referencia',null=True)
    value1 = models.DecimalField("Valor 1",decimal_places=3,max_digits=9,null=True)
    value2 = models.DecimalField("Valor 2",decimal_places=3,max_digits=9,null=True)
    modifier = models.ForeignKey(User)
    createDate = models.DateTimeField("Fecha de creación",auto_now_add=True,null=True)
    modifyDate = models.DateTimeField("Fecha de modificación",null=True)

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
        return self.contactName