# -*- encoding: utf-8 -*-
import json
import mercadopago
from datetime import timedelta

CLIENT_ID = "3061494777347016"
CLIENT_SECRET = "udMUdXsu60e4cEvlm9KcuRU2Jbx9HHPN"
mp = mercadopago.MP(CLIENT_ID, CLIENT_SECRET)

def format_mptime(time, delta=None,zone='-04:00'):
    if delta:
        time = time+timedelta(days=delta)
    s = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+zone
    return s

def _getPaymentMethod():
    return mp.get ("/v1/payment_methods")

def _getReceivedPayments():
    return mp.get ("/v1/payments/search?collector.id=me")    

def _getPreference(preferenceID):
    return mp.get_preference(preferenceID)

def _searchPayments():
    filters = {"id": None, "site_id": None,"external_reference": None}
    searchResult = mp.search_payment(filters)
    return searchResult

def _getPaymentData(paymentID):
    paymentInfo = mp.get_payment(paymentID)
    if paymentInfo["status"] == 200:
        return paymentInfo
    else:
        return None
