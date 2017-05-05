# -*- coding: utf-8 -*-
from django import forms
from ourAdmin.models import Prod

class ProdForm(forms.ModelForm):
    """
    Ceate or modify a Prod 
    """

    class Meta:
        model = Prod
        exclude = ['createDate','modifyDate']

    def __init__(self, *args, **kwargs):
        super(ProdForm, self).__init__(*args, **kwargs)
        for key in self.fields:

            self.fields[key].widget.attrs.update({
                'class': 'form-control'
            })
