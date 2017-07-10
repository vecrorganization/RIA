import json
# Django
from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.views.generic import View,TemplateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
# Project
from ourAdmin.models import Prod
from ourWeb.models import ProdOrder
from ourWeb.forms import *

def home(request):
    return render(request, 'ourWeb/home.html')

class Products(LoginRequiredMixin,TemplateView):
    """
    Show all products
    """
    template_name = 'ourWeb/products.html'
    title = "Compra"

    def products(self):
        return Prod.objects.all()

class ProdDetail(LoginRequiredMixin,TemplateView):
    """
    Show product details
    """
    template_name = 'ourWeb/prod-detail.html'
    title = "Producto"

    def get_context_data(self, **kwargs):
        context = super(ProdDetail, self).get_context_data(**kwargs)
        context['obj'] = get_object_or_404(Prod, id=kwargs['pk'])
        return context


class OrderUserShow(LoginRequiredMixin,TemplateView):
    """
    Show actual user order
    """
    template_name = 'ourWeb/order-user.html'
    title = "Carrito"

    def prodOrder(self):
        return ProdOrder.objects.filter(
                    order = self.request.user.profile.get_order())

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
            post_values['qty'] = int(post_values['qty']) + prod.qty
            form = ProdOrderForm(post_values,instance=prod)
            msg = 'El producto fue actualizado satisfactoriamente.'
        except ObjectDoesNotExist:
            form = ProdOrderForm(post_values)
            msg = 'Producto añadido al carrito.'

        if form.is_valid():
            form.save()
            return JsonResponse(data={'success':True,'msg':msg})

        return JsonResponse(data={'success':False,'msg':'Error: no se ha podido añadir el producto'})

class ProdOrderDelete(LoginRequiredMixin, View):
    """
    Delete a product from user order 
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        try:
            prod = ProdOrder.objects.get(pk=int(post_values['pk']))
            prod.delete()
            data={'deleted':True,'msg':'El producto ha sido eliminado.'}
        except:
            data={'deleted':False,'msg':'Error: no se pudo eliminar el producto.'}

        print(data)
        return JsonResponse(data=data)