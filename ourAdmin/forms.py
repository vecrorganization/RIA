# -*- coding: utf-8 -*-
from django import forms
from ourAdmin.models import Prod

class ProdForm(forms.ModelForm):
    """
    Create or modify a Prod 
    """

    class Meta:
        model = Prod
        exclude = ['createDate','modifyDate']

    def __init__(self, *args, **kwargs):
        super(ProdForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            if self.fields[key].required:
                self.fields[key].widget.attrs['required'] = 'True'
            self.fields[key].widget.attrs.update({
                'class': 'form-control'
            })