import json
# Django
from django.shortcuts import render, redirect
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
    return redirect('Products') #render(request, 'ourWeb/home.html')

class Products(TemplateView):
    """
    Show all products
    """
    template_name = 'ourWeb/products.html'
    title = "Compra"

    def products(self):
        return Prod.objects.all()

    def categories(self):
        from ourAdmin.models import Table
        return Table.objects.filter(type=Table.CATEGORY)


class ProdDetail(TemplateView):
    """
    Show product details
    """
    template_name = 'ourWeb/prod-detail.html'
    title = "Producto"

    def get_context_data(self, **kwargs):
        context = super(ProdDetail, self).get_context_data(**kwargs)
        obj = get_object_or_404(Prod, id=kwargs['pk'])
        context['obj'] = obj
        context['images'] =  obj.get_images()
        return context


class OrderUserShow(LoginRequiredMixin,TemplateView):
    """
    Show actual user order
    """
    template_name = 'ourWeb/order-user.html'
    title = "Carrito"

    def order(self):
        return self.request.user.profile.get_order()

class ProdOrderAdd(LoginRequiredMixin, View):
    """
    Add new product to user order or update a existing one
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        order = request.user.profile.get_order()
        post_values['order'] = order.id

        if int(post_values['qty']) < 1:
            return JsonResponse(data={'success':False,'msg':'Error: la cantidad debe ser mayor a cero.'})

        try:
            prod = ProdOrder.objects.get(order=order,prod_id=post_values['prod'])
            post_values['qty'] = int(post_values['qty']) + prod.qty
            form = ProdOrderForm(post_values,instance=prod)
            msg = 'El producto fue actualizado satisfactoriamente.'
        except ObjectDoesNotExist:
            form = ProdOrderForm(post_values)
            msg = 'Producto añadido al carrito.'

        if form.is_valid():
            prod = form.save()
            return JsonResponse(data={ 'success':True, 'msg':msg})

        return JsonResponse(data={'success':False,'msg':'Error: no se ha podido añadir el producto'})

class ProdOrderUpdate(LoginRequiredMixin, View):
    """
    Update product 
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        order = request.user.profile.get_order()
        post_values['order'] = order.id

        try:
            prod = ProdOrder.objects.get(order=order,prod_id=post_values['prod'])
            form = ProdOrderForm(post_values,instance=prod)
            msg = 'El producto fue actualizado satisfactoriamente.'
        except ObjectDoesNotExist:
            return JsonResponse(data={'success':False,'msg':'Error: no se ha podido actualizar el producto.'})

        if form.is_valid():
            prod = form.save()
            return JsonResponse(data={
                                    'success':True,
                                    'msg':msg,
                                    'qty':prod.qty,
                                    'prod_total':prod.get_total_amount(),
                                    'id':prod.id,
                                    'total':prod.order.total
                                    })

        return JsonResponse(data={'success':False,'msg':'Error: la cantidad del producto debe ser mayor a 0.'})

class ProdOrderDelete(LoginRequiredMixin, View):
    """
    Delete a product from user order 
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        pk = int(post_values['pk'])
        try:
            prod = ProdOrder.objects.get(pk=pk)
            prod.delete()
            data={'deleted':True,'msg':'El producto ha sido eliminado.','total':prod.order.total,'id':pk}
        except:
            data={'deleted':False,'msg':'Error: no se pudo eliminar el producto.'}

        print(data)
        return JsonResponse(data=data)