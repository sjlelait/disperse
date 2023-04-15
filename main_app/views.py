from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Spot

# Create your views here.
def home(request):
    return render(request, 'home.html')



class SpotList(ListView):
    model = Spot
    fields = '__all__'
    template_name = 'spots/spot_list.html'