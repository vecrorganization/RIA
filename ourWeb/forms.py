# -*- coding: utf-8 -*-
from django import forms
from ourWeb.models import Order,ProdOrder

class OrderForm(forms.ModelForm):
    """
    Create or modify a Order
    """

    class Meta:
        model = Order
        exclude = []

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control'
            })

class ProdOrderForm(forms.ModelForm):
    """
    Create or modify a ProdOrder
    """
    class Meta:
        model = ProdOrder
        exclude = []

    def clean(self):
        cleaned_data = super(ProdOrderForm, self).clean()
        qty = cleaned_data.get('qty')

        if qty < 1:
            self.add_error('date_from', 'La cantidad debe ser mayor a 0.')