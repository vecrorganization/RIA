# -*- coding: utf-8 -*-
from django import forms
from ourAdmin.models import Prod, Table

class ProdForm(forms.ModelForm):
    """
    Ceate or modify a Prod 
    """
    category = forms.ModelChoiceField(queryset= Table.objects.filter(type=Table.CATEGORY))
    clase = forms.ModelChoiceField(queryset= Table.objects.filter(type=Table.CLASS))
    tax1 = forms.ModelChoiceField(queryset= Table.objects.filter(type=Table.TAX))
    tax2 = forms.ModelChoiceField(queryset= Table.objects.filter(type=Table.TAX))

    class Meta:
        model = Prod
        exclude = ['createDate','modifyDate','modifier']

    def __init__(self, *args, **kwargs):
        super(ProdForm, self).__init__(*args, **kwargs)
        for key in self.fields:

            self.fields[key].widget.attrs.update({
                'class': 'form-control'
            })

class TableForm(forms.ModelForm):
    """
    Ceate or modify a Table
    """

    class Meta:
        model = Table
        exclude = ['modifier','createDate','modifyDate']

    def __init__(self, *args, **kwargs):
        super(TableForm, self).__init__(*args, **kwargs)
        for key in self.fields:

            self.fields[key].widget.attrs.update({
                'class': 'form-control'
            })