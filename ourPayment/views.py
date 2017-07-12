# -*- encoding: utf-8 -*-
import json
# Django
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib import messages

# Project
import os, sys
import mercadopago

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
