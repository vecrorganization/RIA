# -*- coding: utf-8 -*-
import json
from datetime import datetime
# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from braces.views import LoginRequiredMixin,StaffuserRequiredMixin
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User

# Project
import os, sys
import mercadopago
from ourWeb.models import ProdOrder
from ourAuth.models import AddressUser
from ourAdmin.models import Address
from ourAdmin.forms import AddressForm

def MPTest(req, **kwargs):
    """
    MP Test
    """
    CLIENT_ID = "4815438540890951"
    CLIENT_SECRET = "OHuCBlVIxzUki07MaRYXpW4wWdxl9g0y"
    mp = mercadopago.MP(CLIENT_ID, CLIENT_SECRET)

    preference = {
    "items": [
        {
            "id": "item-ID-1234",
            "title": "Zapatillas converse negras.",
            "currency_id": "VEF",
            "picture_url": "http://s-media-cache-ak0.pinimg.com/originals/67/cd/a7/67cda74fd6eaf631b28fd9f8efd19412.gif",
            "description": "Item descriptionsaffffffffffffffffffffffffffffffffffffffffffffffffff",
            "category_id": "art", # Available categories at https://api.mercadopago.com/item_categories
            "quantity": 1,
            "unit_price": 100
        },
        {
            "id": "item-ID-2234",
            "title": "Zapatillas converse blancas.",
            "currency_id": "VEF",
            "picture_url": "http://mercadoentucasa.com/photos/product/2/174/2.jpg",
            "description": "Item dffffffffffffffffffffffffffffff",
            "category_id": "art", # Available categories at https://api.mercadopago.com/item_categories
            "quantity": 3,
            "unit_price": 100
        }
    ],
    "payer": {
        "name": "user-name",
        "surname": "user-surname",
        "email": "user@email.com",
        "date_created": "2015-06-02T12:58:41.425-04:00",
        "phone": {
            "area_code": "11",
            "number": "4444-4444"
        },
        "identification": {
            "type": "CI-V", # Available ID types at https://api.mercadopago.com/v1/identification_types
            "number": "12345678"
        },
        "address": {
            "street_name": "Street",
            "street_number": 123,
            "zip_code": "5700"
        } 
    },
    "back_urls": {
        "success": "https://www.success.com",
        "failure": "http://www.failure.com",
        "pending": "http://www.pending.com"
    },
    "auto_return": "approved",
    "payment_methods": {
        "excluded_payment_methods": [
            {
                "id": "master"
            }
        ],
        "excluded_payment_types": [
            {
                "id": "ticket"
            }
        ],
        "installments": 12,
        "default_payment_method_id": 'null',
        "default_installments": 'null'
    },
    "shipments": {
        "receiver_address": {
            "zip_code": "5700",
            "street_number": 123,
            "street_name": "Street",
            "floor": 4,
            "apartment": "C"
        }
    },
    "notification_url": "https://www.your-site.com/ipn",
    "external_reference": "Reference_1234",
    "expires": True,
    "expiration_date_from": "2016-02-01T12:00:00.000-04:00",
    "expiration_date_to": "2019-02-28T12:00:00.000-04:00"
    }




    preferenceResult = mp.create_preference(preference)

    url = preferenceResult["response"]["sandbox_init_point"]

    output = """
    <!doctype html>
    <html>
        <head>
            <title>Pay</title>
        </head>
        <body>
            <a href="{url}">Pay</a>
        </body>
    </html>
    """.format (url=url)


    return HttpResponse(output)

class PurchaseSummary(LoginRequiredMixin,TemplateView):
    """
    Summary of purchase
    """
    template_name = 'ourPayment/summary.html'

    def get_context_data(self, **kwargs):
        context = super(PurchaseSummary, self).get_context_data(**kwargs)
        context['addresses'] = AddressUser.objects.filter(user = self.request.user)
        context['Title'] = "Información de pago"

        return context



class PaymentAddress(LoginRequiredMixin,TemplateView):
    """
    Fill information needed for purchase
    IMPORTANTE : Si address no es mia no lo puedo modificar
    """

    template_name = 'ourPayment/address.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentAddress, self).get_context_data(**kwargs)
        if 'pk' in kwargs:
            address = get_object_or_404(Address, id=int(kwargs['pk']))
            context['form'] = AddressForm(instance=address)
            context['Title'] = "Modificar Dirección"
            context['pk'] = int(kwargs['pk'])
        else:
            context['form'] = AddressForm()
            context['Title'] = "Registrar dirección"
        return context

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        if 'pk' in kwargs:
            address = get_object_or_404(Address, id=int(kwargs['pk']))
            form = AddressForm(post_values,instance=address)
            title = "Modificar Dirección"
            msg = "Modificación realizada"
        else:
            form = AddressForm(post_values)
            title = "Crear Dirección"
            msg = "Creación exitosa"

        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, msg)
            address = form.save()
            if not 'pk' in kwargs:
                AddressUser.objects.create(user = request.user, address = address)
        else:
            messages.add_message(request, messages.ERROR, 'Error: no se realizo la operación')
            return render(request, self.template_name, {'form':form,'Title':title})

        return redirect('PurchaseSummary')


class PayMp(LoginRequiredMixin,TemplateView):
    """
    Pay using Mercado Pago
    segurar
    """

    template_name = 'ourPayment/pay.html'

    def get_context_data(self, **kwargs):
        context = super(PayMp, self).get_context_data(**kwargs)
        order = self.request.user.profile.get_order()

        if 'pk' in kwargs:
            address = get_object_or_404(Address, id=int(kwargs['pk']))
            order.address = address
            order.save()
        else:
            #404
            None       


        products = ProdOrder.objects.filter(order = order)
        context['Title'] = "Confirmar orden"
        context['order'] = order
        context['products'] = products
        context['date'] = datetime.today()
        return context