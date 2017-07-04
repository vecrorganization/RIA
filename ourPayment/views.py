# -*- encoding: utf-8 -*-
import json
# Django
from django.shortcuts import render, HttpResponse
from braces.views import LoginRequiredMixin
from django.views.generic import View,TemplateView
from django.http import JsonResponse
from django.contrib import messages

# Project
import os, sys
import mercadopago

def MPTest(req, **kwargs):
    """
    MP Test
    """
    preference = {
        "items": [
            {
                "title": "Multicolor kite",
                "quantity": 1,
                "currency_id": "VEF", # Available currencies at: https://api.mercadopago.com/currencies
                "unit_price": 10.0
            }
        ]
    }
    mp = mercadopago.MP("1763747719632056", "7RLFXjDKjZcIThVw5B7n5vE727w8A6ca")

    preferenceResult = mp.create_preference(preference)

    url = preferenceResult["response"]["init_point"]

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