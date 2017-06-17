# Django
from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.views.generic import View
# Project
from ourWeb.models import ProdOrder
from ourWeb.forms import *

def home(request):
    return render(request, 'ourWeb/home.html')

class ProdOrderAddUpdate(LoginRequiredMixin, View):
    """
    Add new product to user order or update a existing one
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        order = user.profile.get_order()
        post_values['order'] = order.id

        try:
            prod = ProdOrder.objects.get(order=order,prod_id=post_values['prod_id'])
            form = ProdOrderForm(post_values,instance=prod)
        except:
            form = ProdOrderForm(post_values)

        if form.is_valid:
            form.save()
            return JsonResponse(data={'success':True})

        return JsonResponse(data={'success':False})

class ProdOrderDelete(LoginRequiredMixin, View):
    """
    Delete a product from user order 
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        ProdOrder.objects.get(order_id=post_values['order_id'],prod_id=post_values['prod_id']).delete()
        return JsonResponse(data={'success':True})