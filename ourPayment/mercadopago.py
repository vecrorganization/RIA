# -*- encoding: utf-8 -*-
import json
import mercadopago

CLIENT_ID = "4815438540890951"
CLIENT_SECRET = "OHuCBlVIxzUki07MaRYXpW4wWdxl9g0y"
mp = mercadopago.MP(CLIENT_ID, CLIENT_SECRET)

def _getPaymentMethod():
    return mp.get ("/v1/payment_methods")

def _getPreference(preferenceID):
    return mp.get_preference(preferenceID)

def _searchPayments():
    filters = {
        "id": None,
        "site_id": None,
        "external_reference": None
    }

    return mp.search_payment(filters)  

def _getPaymentData(paymentID):
    paymentInfo = mp.get_payment(paymentID)
    print(paymentInfo)
    if paymentInfo["status"] == 200:
        return paymentInfo
    else:
        return None
