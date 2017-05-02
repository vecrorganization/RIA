# Django
import random
import json
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
# from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, View
# App