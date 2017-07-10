# -*- coding: utf-8 -*-
from django import forms
from ourAdmin.models import Prod, Table, Address

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
        widgets = {
          'desc': forms.Textarea(attrs={'rows':4, 'cols':15,'style':'resize:none;'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProdForm, self).__init__(*args, **kwargs)
        for key in (x for x in self.fields if x not in ["image_"+str(i) for i in range(1,6)]):
            self.fields[key].widget.attrs.update({
                'class': 'form-control'
            })
        for key in ["image_"+str(i) for i in range(1,6)]:
            self.fields[key].widget.attrs.update({
                'class': 'image'
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
    def clean(self):
        cleaned_data = super(TableForm, self).clean()
        ttype = cleaned_data.get('type')
        if ttype == Table.TAX:
            value1 = cleaned_data.get('value1')
            if not value1:
                self.add_error('value1', "El campo de value1 no puede estar vacío al crear un tax.")

        elif ttype == Table.STATE:
            refer = cleaned_data.get('refer')
            if not refer:
                self.add_error('refer', "El campo de refer no puede estar vacío al crear un estado.")
            elif (refer.type != Table.COUNTRY):
                self.add_error('refer', "El campo de refer debe ser de tipo country.")

class AddressForm(forms.ModelForm):
    """
    Create or modify a Address
    """
    state = forms.ModelChoiceField(queryset= Table.objects.filter(type=Table.STATE))

    class Meta:
        model = Address
        exclude = []

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control'
            })