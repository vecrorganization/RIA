# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico'
        }

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data.get('email')

        if not email:
            self.add_error('email', "El campo de correo no puede estar vacío.")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        for key in self.fields:
            self.fields[key].help_text = None
            self.fields[key].widget.attrs.update({
                'class': 'form-control'
            })