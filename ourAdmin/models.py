# -*- encoding: utf-8 -*-

from datetime import date
# Django
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Table(models.Model):
    TAX = "T"
    CATEGORY = "C"

    TYPE_CHOICES = (
        (TAX, 'Tax'),
        (CATEGORY, 'Category')
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