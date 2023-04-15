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



class SpotList(LoginRequiredMixin, ListView):
    model = Spot
    fields = '__all__'
    template_name = 'spots/spot_list.html'

class SpotDetail(LoginRequiredMixin, DetailView):
    model = Spot
    fields = '__all__'
    template_name = 'spots/spot_detail.html'

class SpotUpdate(LoginRequiredMixin, UpdateView):
    model = Spot
    fields = ['name', 'description', 'zipcode', 'latitude', 'longitude']
    template_name = 'spots/spot_form.html'

class SpotDelete(LoginRequiredMixin, DeleteView):
    model = Spot
    success_url = '/spots/'
    template_name = 'spots/spot_confirm_delete.html'

class SpotCreate(CreateView):
  model = Spot
  fields = ['name', 'description', 'zipcode', 'latitude', 'longitude']
  template_name = 'spots/spot_form.html'
  def form_valid(self, form):
    form.instance.user = self.request.user 
    return super().form_valid(form)