# -*- coding: utf-8 -*-
import json
# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
#from django.contrib import messages
#from django.core.urlresolvers import reverse
#from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView, View
# App
from ourAdmin.models import Prod
from ourAdmin.forms import ProdForm

class ProdSearch(TemplateView):
    """
    Search a Prod 
    """

    template_name = 'ourAdmin/prod/search.html'

    def get_context_data(self, **kwargs):
        context = super(ProdSearch, self).get_context_data(**kwargs)
        context['Title'] = "Buscar producto"
        return context

class ProdSearchAjax(View):
    """
    Get and send ajax with the product searching
    """

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        prods = []
        if 'id' in post_values:
            try:
                prods = [Prod.objects.get(id=int(post_values['id']))]
            except:
                pass
        elif 'name' in post_values and not prods:
            prods = Prod.objects.filter(name__icontains=int(post_values['name']))

        data = [{'pk': prod.id, 'name': prod.name} for prod in prods]
        return HttpResponse(json.dumps(data), content_type='application/json')


class ProdCreateModify(TemplateView):
    """
    Create or modify a Prod 
    """

    template_name = 'ourAdmin/prod/create-modify.html'

    def get_context_data(self, **kwargs):
        context = super(ProdCreateModify, self).get_context_data(**kwargs)
        if 'pk' in kwargs:
            prod = get_object_or_404(Prod, id=int(kwargs['pk']))
            context['form'] = ProdForm(instance=prod)
            context['Title'] = "Modificar Prod"
        else:
            context['form'] = ProdForm()
            context['Title'] = "Crear Prod"

        return context

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        if 'pk' in kwargs:
            prod = get_object_or_404(Prod, id=int(kwargs['pk']))
            form = ProdForm(post_values,instance=prod)
            title = "Modificar Prod"
        else:
            form = ProdForm(post_values)
            title = "Crear Prod"

        if form.is_valid():
            prod = form.save()
        else:
            return render_to_response(template_name, {'form':form,'Title':title},
                                      context_instance=RequestContext(request))

        return redirect('ProdSearch')  