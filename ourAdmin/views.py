# -*- coding: utf-8 -*-
# Django
from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib import messages
#from django.core.urlresolvers import reverse
#from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
# App
from ourAdmin.models import Prod
from ourAdmin.forms import ProdForm

class ProdCreateModify(TemplateView):
    """
    Create or modify a Prod 
    """

    template_name = 'ourAdmin/prod/create-modify.html'

    def get_context_data(self, **kwargs):
        context = super(ProdCreateModify, self).get_context_data(**kwargs)
        if 'pk' in kwargs:
            prod = get_object_or_404(Prod, id=int(post_values['pk']))
            context['form'] = ProdForm(instance=prod)
            context['Title'] = "Modificar Prod"
        else:
            context['form'] = ProdForm()
            context['Title'] = "Crear Prod"

        return context

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        if 'pk' in kwargs:
            prod = get_object_or_404(Prod, id=int(post_values['pk']))
            form = ProdForm(post_values,instance=prod)
        else:
            form = ProdForm(post_values)

        if form.is_valid():
            prod = form.save()
        else:
            return render_to_response(template_name, {'form':form},
                                      context_instance=RequestContext(request))

        return redirect('ProdCreate')  #cambiar por Producto 001