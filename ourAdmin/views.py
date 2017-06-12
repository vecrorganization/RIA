# -*- coding: utf-8 -*-
import json
from datetime import datetime
# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from braces.views import LoginRequiredMixin,StaffuserRequiredMixin
from django.views.generic import TemplateView, View
# App
from ourAdmin.models import Prod, Table, Order, Address, Payment
from ourAdmin.forms import ProdForm, TableForm, OrderForm, AddressForm


class Home(LoginRequiredMixin,StaffuserRequiredMixin,TemplateView):
    """
    Our Admin Home
    """
    template_name = 'ourAdmin/home.html'

########################################################################################
    

class ProdSearch(LoginRequiredMixin,StaffuserRequiredMixin,TemplateView):
    """
    Search a Prod 
    """

    template_name = 'ourAdmin/prod/search.html'

    def get_context_data(self, **kwargs):
        context = super(ProdSearch, self).get_context_data(**kwargs)
        context['Title'] = "Buscar producto"
        return context


class ProdSearchAjax(LoginRequiredMixin,StaffuserRequiredMixin,View):
    """
    Get and send ajax with the product searching
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        prods = []

        if 'id' in post_values and post_values['id']:
            prods = Prod.objects.filter(id__icontains=post_values['id'])
            if 'name' in post_values and post_values['name']:
                prods = prods.filter(name__icontains=post_values['name'])
        elif 'name' in post_values and post_values['name']:
            prods = Prod.objects.filter(name__icontains=post_values['name'])

        data = [{'pk': prod.id, 'name': prod.name} for prod in prods]
        return HttpResponse(json.dumps(data), content_type='application/json')

class ProdDeleteAjax(LoginRequiredMixin,StaffuserRequiredMixin,View):
    """
    Delete requested Prod
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        try:
            Prod.objects.get(id = post_values['pk']).delete()
            messages.add_message(request, messages.SUCCESS, 'Se elimino correctamente')
            data={'deleted' : 1}
        except:
            messages.add_message(request, messages.ERROR, 'Error: no se realizo la operación')
            data={'deleted' : 0}
        
        return HttpResponse(json.dumps(data), content_type='application/json')

class ProdCreateModify(LoginRequiredMixin,StaffuserRequiredMixin,TemplateView):
    """
    Create or modify a Prod 
    """

    template_name = 'ourAdmin/prod/create-modify.html'

    def get_context_data(self, **kwargs):
        context = super(ProdCreateModify, self).get_context_data(**kwargs)
        if 'pk' in kwargs:
            prod = get_object_or_404(Prod, id=kwargs['pk'])
            context['form'] = ProdForm(instance=prod)
            context['Title'] = "Modificar Producto"
        else:
            context['form'] = ProdForm()
            context['Title'] = "Crear Producto"

        return context

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        if 'pk' in kwargs:
            prod = get_object_or_404(Prod, id=kwargs['pk'])
            form = ProdForm(post_values,request.FILES,instance=prod)
            title = "Modificar Producto"
            msg = "Modificación realizada"
        else:
            form = ProdForm(post_values,request.FILES)
            title = "Crear Producto"
            msg = "Creación exitosa"

        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, msg)
            prod = form.save(commit=False)
            prod.modifier = request.user
            prod.save()

        else:
            messages.add_message(request, messages.ERROR, 'Error: no se realizo la operación')
            return render_to_response(self.template_name, {'form':form,'Title':title},
                                      context_instance=RequestContext(request))

        return redirect('ProdSearch')  

#################################################################################################################


class TableCreateModify(LoginRequiredMixin,StaffuserRequiredMixin,TemplateView):
    """
    Create or modify a Table 
    """

    template_name = 'ourAdmin/table/create-modify.html'

    def get_context_data(self, **kwargs):
        context = super(TableCreateModify, self).get_context_data(**kwargs)
        if 'pk' in kwargs:
            table = get_object_or_404(Table, id=int(kwargs['pk']))
            context['form'] = TableForm(instance=table)
            context['Title'] = "Modificar Table"
            context['pk'] = int(kwargs['pk'])
        else:
            context['form'] = TableForm()
            context['Title'] = "Crear Table"

        return context

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        #user = request.user
        user = User.objects.get(pk=1)
        if 'pk' in kwargs:
            table = get_object_or_404(Table, id=int(kwargs['pk']))
            table.modifier = user
            table.modifyDate = datetime.now()
            form = TableForm(post_values,instance=table)
            title = "Modificar Table"
            msg = "Modificación realizada"
        else:
            table = Table(modifier  = user)
            form = TableForm(post_values,instance=table)
            title = "Crear Table"
            msg = "Creación exitosa"

        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, msg)
            table = form.save()
        else:
            messages.add_message(request, messages.ERROR, 'Error: no se realizo la operación')
            return render(request, self.template_name, {'form':form,'Title':title})

        return redirect('TableSearch')


class TableSearch(LoginRequiredMixin,StaffuserRequiredMixin,TemplateView):
    """
    Search a Table
    """
    template_name = 'ourAdmin/table/search.html'

    def get_context_data(self, **kwargs):
        context = super(TableSearch, self).get_context_data(**kwargs)
        context['Title'] = "Buscar tabla"
        context['t_choices'] = Table.TYPE_CHOICES
        return context


class TableSearchAjax(LoginRequiredMixin,StaffuserRequiredMixin,View):
    """
    Get and send ajax with the table searching
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()

        if post_values['type']:
            tables = Table.objects.filter( type= post_values['type'] )
            if post_values['desc']:
                tables = tables.filter(desc__icontains=post_values['desc'])

        else:
             tables = Table.objects.filter(desc__icontains=post_values['desc'])

        data = [{'pk': t.pk, 'type': t.type, 'desc': t.desc} for t in tables]
        
        return HttpResponse(json.dumps(data), content_type='application/json')

class TableDeleteAjax(LoginRequiredMixin,StaffuserRequiredMixin,View):
    """
    Delete requested table
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        print(post_values)
        try:
            Table.objects.get(id = int(post_values['pk'])).delete()
            messages.add_message(request, messages.SUCCESS, 'Se elimino correctamente')
            data={'deleted' : 1}
        except:
            messages.add_message(request, messages.ERROR, 'Error: no se realizo la operación')
            data={'deleted' : 0}
        
        return HttpResponse(json.dumps(data), content_type='application/json')



################################################################################################

class OrderCreateModify(LoginRequiredMixin,StaffuserRequiredMixin,TemplateView):
    """
    Create or modify a Order 
    """

    template_name = 'ourAdmin/order/create-modify.html'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateModify, self).get_context_data(**kwargs)
        if 'pk' in kwargs:
            order = get_object_or_404(Order, id=int(kwargs['pk']))
            context['form'] = OrderForm(instance=order)
            context['Title'] = "Modificar Order"
            context['pk'] = int(kwargs['pk'])
        else:
            context['form'] = OrderForm()
            context['Title'] = "Crear Order"

        return context

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        if 'pk' in kwargs:
            order = get_object_or_404(Order, id=int(kwargs['pk']))
            form = OrderForm(post_values,instance=order)
            title = "Modificar Order"
            msg = "Modificación realizada"
        else:
            form = OrderForm(post_values)
            title = "Crear Order"
            msg = "Creación exitosa"

        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, msg)
            order = form.save()
        else:
            messages.add_message(request, messages.ERROR, 'Error: no se realizo la operación')
            return render(request, self.template_name, {'form':form,'Title':title})

        return redirect('OrderSearch')


class OrderSearch(LoginRequiredMixin,StaffuserRequiredMixin,TemplateView):
    """
    Search a Order
    """
    template_name = 'ourAdmin/order/search.html'

    def get_context_data(self, **kwargs):
        context = super(OrderSearch, self).get_context_data(**kwargs)
        context['Title'] = "Buscar Order"
        context['s_choices'] = Order.STATUS_CHOICES
        return context


class OrderSearchAjax(LoginRequiredMixin,StaffuserRequiredMixin,View):
    """
    Get and send ajax with the order searching
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        orders = []

        try:
            #search by id
            orders = [Order.objects.get(id=int(post_values['id']))]
        except:
            #search by status if it is not ""
            if 'status' in post_values and post_values['status']:
                orders = Order.objects.filter(status__icontains=post_values['status'])

        data = [{'pk': order.id, 'status': order.get_status_display()} for order in orders]
        return HttpResponse(json.dumps(data), content_type='application/json')


class OrderDeleteAjax(LoginRequiredMixin,StaffuserRequiredMixin,View):
    """
    Delete requested order
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        print(post_values)
        try:
            Order.objects.get(id = int(post_values['pk'])).delete()
            messages.add_message(request, messages.SUCCESS, 'Se elimino correctamente')
            data={'deleted' : 1}
        except:
            messages.add_message(request, messages.ERROR, 'Error: no se realizo la operación')
            data={'deleted' : 0}
        
        return HttpResponse(json.dumps(data), content_type='application/json')


################################################################################################

class AddressCreateModify(LoginRequiredMixin,StaffuserRequiredMixin,TemplateView):
    """
    Create or modify a Address
    """

    template_name = 'ourAdmin/address/create-modify.html'

    def get_context_data(self, **kwargs):
        context = super(AddressCreateModify, self).get_context_data(**kwargs)
        if 'pk' in kwargs:
            address = get_object_or_404(Address, id=int(kwargs['pk']))
            context['form'] = AddressForm(instance=address)
            context['Title'] = "Modificar Dirección"
            context['pk'] = int(kwargs['pk'])
        else:
            context['form'] = AddressForm()
            context['Title'] = "Crear Dirección"

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
        else:
            messages.add_message(request, messages.ERROR, 'Error: no se realizo la operación')
            return render(request, self.template_name, {'form':form,'Title':title})

        return redirect('AddressSearch')


class AddressSearch(LoginRequiredMixin,StaffuserRequiredMixin,TemplateView):
    """
    Search a Address
    """
    template_name = 'ourAdmin/address/search.html'

    def get_context_data(self, **kwargs):
        context = super(AddressSearch, self).get_context_data(**kwargs)
        context['Title'] = "Buscar Dirección"
        context['s_choices'] = Address.STATE_CHOICES
        return context


class AddressSearchAjax(LoginRequiredMixin,StaffuserRequiredMixin,View):
    """
    Get and send ajax with the address searching
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()

        if 'state' in post_values and post_values['state']:
            address = Address.objects.filter( state__icontains = post_values['state'])
            if 'dir' in post_values and post_values['dir']:
                address = address.filter(address1__icontains=post_values['dir']) | address.filter(address2__icontains=post_values['dir'])
        elif 'dir' in post_values and post_values['dir']:
            address = Address.objects.filter(address1__icontains=post_values['dir']) | Address.objects.filter(address2__icontains=post_values['dir'])

        data = [{'pk': addr.pk, 'addr': str(addr)} for addr in address]
        print(data)
        return HttpResponse(json.dumps(data), content_type='application/json')


class AddressDeleteAjax(LoginRequiredMixin,StaffuserRequiredMixin,View):
    """
    Delete requested address
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        try:
            Address.objects.get(id = int(post_values['pk'])).delete()
            messages.add_message(request, messages.SUCCESS, 'Se elimino correctamente')
            data={'deleted' : 1}
        except:
            messages.add_message(request, messages.ERROR, 'Error: no se realizo la operación')
            data={'deleted' : 0}
        
        return HttpResponse(json.dumps(data), content_type='application/json')


##########################################################################

class PaymentSearch(LoginRequiredMixin,StaffuserRequiredMixin,TemplateView):
    """
    Search a Payment 
    """

    template_name = 'ourAdmin/payment/search.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentSearch, self).get_context_data(**kwargs)
        context['Title'] = "Buscar pago"
        return context


class PaymentAjax(LoginRequiredMixin,StaffuserRequiredMixin,View):
    """
    Get and send ajax with the payment searching
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        payments = []

        if 'order' in post_values and post_values['order']:
            payments = Payment.objects.filter(order_id=int(post_values['order']))
        elif 'date' in post_values and post_values['date']:
            date = datetime.strptime(post_values['date'], '%d/%m/%Y').strftime('%Y-%m-%d')
            payments = Payment.objects.filter(date=date)

        data = [{'pk': p.id, 
                'date': p.date.strftime('%d/%m/%Y'), 
                'order': p.order.id,
                'paymentMethod':p.paymentUser.paymentMethod.cardType,
                'user':p.paymentUser.user.get_full_name()} for p in payments]
        return HttpResponse(json.dumps(data), content_type='application/json')