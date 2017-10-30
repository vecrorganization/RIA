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
import ourPayment.mercadopago as mercadopago
from ourWeb.models import ProdOrder
from ourAuth.models import AddressUser
from ourAdmin.models import Address, PaymentMethod
from ourAdmin.forms import AddressForm
from ourWeb.models import Order

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

        return redirect('ManageAddress')

#############################IPN (Notificaciones de pago)#############################################
class SuccessMP(LoginRequiredMixin,TemplateView):
    template_name = 'ourPayment/success.html'
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        qd = request.GET
        collection_id = qd.get("collection_id")
        payment_type = qd.get("payment_type")

        payment = mercadopago._getPaymentData(collection_id)
        payment = payment['response']['collection']

        if payment['status'] == 'approved':
            #Order
            order_id = payment['external_reference']
            order = Order.objects.get(id=int(order_id))
            order.status = Order.COMPLETED
            order.date = datetime.now()
            order.save()
            print(order.status)
            
            #Payment


            #context
            products = ProdOrder.objects.filter(order = order)
            context['products'] = products
            context['payment'] = payment
            context['order'] = order
            context['Title'] = "Resumen pago"
        return self.render_to_response(context)


class PendingMP(LoginRequiredMixin,TemplateView):
    
    def get (self, request):
        pass

def IpnMP(req, **kwargs):

    pass
    '''topic = kwargs["topic"]
    merchant_order_info = None

    if topic == "payment":
        payment_info = mercadopago.mp.get("/collections/notifications/"+kwargs["id"])
        merchant_order_info = mercadopago.mp.get("/merchant_orders/"+payment_info["response"]["collection"]["merchant_order_id"])
        print(merchant_order_info)
    elif topic == "merchant_order":
        merchant_order_info = mercadopago.mp.get("/merchant_orders/"+kwargs["id"])
        print(merchant_order_info)
    if merchant_order_info == None:
        raise ValueError("Error obtaining the merchant_order")

    if merchant_order_info["status"] == 200:
        return {
            "payment": merchant_order_info["response"]["payments"],
            "shipment": merchant_order_info["response"]["shipments"]
        }
    '''
########################################################################################################################

class PayMp(LoginRequiredMixin,TemplateView):
    """
    Pay using Mercado Pago
    segurar
    """

    template_name = 'ourPayment/pay.html'

    def get_context_data(self, **kwargs):
        context = super(PayMp, self).get_context_data(**kwargs)
        order = self.request.user.profile.get_order()
        order.update_total()

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

        
        desc = ""
        for p in products:
            desc = desc + " "+p.prod.name + " x " + str(p.qty) + ","
        desc = desc[:-1]

        items = []
        for p in products:
            items.append({
                    "id": str(p.prod.id),
                    "title": desc,
                    "currency_id": "VEF",
                    "picture_url": p.prod.image_1.url,
                    "description": p.prod.desc,
                    "category_id": "art", # Available categories at https://api.mercadopago.com/item_categories
                    "quantity": p.qty,
                    "unit_price": float(p.prod.price)+ float(p.prod.get_tax())
                })

        payer = {
            "name": self.request.user.first_name,
            "surname": self.request.user.last_name,
            "email": self.request.user.email,
            "date_created": str(datetime.now()),
            "phone": {
                "area_code": "11",
                "number": address.telephone
            },
            "identification": {
                "type": "CI-V", # Available ID types at https://api.mercadopago.com/v1/identification_types
                "number": "12345678"
            },
            "address": {
                "street_name": address.address1,
                "street_number": 123,
                "zip_code": address.zipCode
            } 
        }

        preference = {
        "items": items,
        "payer": payer,
        "back_urls": {
            "success": "https://ria-development.herokuapp.com/payment/success",
            "failure": "https://ria-development.herokuapp.com/userorder/",
            "pending": "https://ria-development.herokuapp.com/payment/pending"
        },
        "auto_return": "approved",
        "payment_methods": {
            "installments": 12,
            "default_payment_method_id": 'null',
            "default_installments": 'null'
        },
        "notification_url": "https://ria-development.herokuapp.com/payment/ipn/",
        "external_reference": order.id,
        "expires": True,
        "expiration_date_from": mercadopago.format_mptime(datetime.now()),
        "expiration_date_to": mercadopago.format_mptime(datetime.now(),27)
        }




        preferenceResult = mercadopago.mp.create_preference(preference)

        url = preferenceResult["response"]["init_point"]
        context['mp_url'] = url

        return context 
