import json
# Django
from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.views.generic import View,TemplateView
from django.http import JsonResponse
from django.contrib import messages
# Project
from ourAdmin.models import Prod
from ourWeb.models import ProdOrder
from ourWeb.forms import *

def home(request):
    return render(request, 'ourWeb/home.html')

class ProdShow(LoginRequiredMixin,TemplateView):
    """
    Show all products
    """
    template_name = 'ourWeb/prod-show.html'

    def get_context_data(self, **kwargs):
        context = super(ProdShow, self).get_context_data(**kwargs)
        context['objs'] = Prod.objects.all()
        context['Title'] = "Compra"
        return context

class OrderUserShow(LoginRequiredMixin,TemplateView):
    """
    Show actual user order
    """
    template_name = 'ourWeb/order-user.html'

    def get_context_data(self, **kwargs):
        context = super(OrderUserShow, self).get_context_data(**kwargs)
        order = self.request.user.profile.get_order()
        context['objs'] = ProdOrder.objects.filter(order = order)
        context['Title'] = "Carrito"
        return context

class ProdOrderAddUpdate(LoginRequiredMixin, View):
    """
    Add new product to user order or update a existing one
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        order = request.user.profile.get_order()
        post_values['order'] = order.id

        try:
            prod = ProdOrder.objects.get(order=order,prod_id=post_values['prod'])
            form = ProdOrderForm(post_values,instance=prod)
        except:
            form = ProdOrderForm(post_values)

        if form.is_valid():
            form.save()
            return JsonResponse(data={'success':True,'msg':'Producto añadido al carrito'})

        return JsonResponse(data={'success':False,'error':'Error: no se ha podido añadir el producto'})

class ProdOrderDelete(LoginRequiredMixin, View):
    """
    Delete a product from user order 
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        try:
            prod = ProdOrder.objects.get(pk=int(post_values['pk']))
            prod.delete()
            msg = "Producto eliminado del carrito"
            messages.add_message(request, messages.SUCCESS, msg)
            return JsonResponse(data={'deleted' : 1})
        except:
            return JsonResponse(data={'deleted' : 0,'error':'Error: no se ha podido eliminar el producto del carrito'})