# -*- coding: utf-8 -*-
import json
# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
#from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin,StaffuserRequiredMixin
from django.views.generic import TemplateView, View
# App
from ourAdmin.models import Prod, Table
from ourAdmin.forms import ProdForm, TableForm
from datetime import datetime


class Home(LoginRequiredMixin,StaffuserRequiredMixin,TemplateView):
    """
    Our Admin Home
    """
    template_name = 'ourAdmin/home.html'
    

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

        try:
            #search by id
            prods = [Prod.objects.get(id=post_values['id'])]
        except:
            #search by name if it is not ""
            if 'name' in post_values and post_values['name']:
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
            context['Title'] = "Modificar Prod"
        else:
            context['form'] = ProdForm()
            context['Title'] = "Crear Prod"

        return context

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        if 'pk' in kwargs:
            prod = get_object_or_404(Prod, id=kwargs['pk'])
            form = ProdForm(post_values,request.FILES,instance=prod)
            title = "Modificar Prod"
            msg = "Modificación realizada"
        else:
            form = ProdForm(post_values,request.FILES)
            title = "Crear Prod"
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
        print(post_values)

        if post_values['type']:
            tables = Table.objects.filter( type= post_values['type'] )
            if post_values['desc']:
                tables = tables.filter(desc__icontains=post_values['desc'])

        else:
             tables = Table.objects.filter(desc__icontains=post_values['desc'])

        data = [{'pk': t.pk, 'type': t.type, 'desc': t.desc} for t in tables]
        print(data)
        
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