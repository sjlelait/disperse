from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Spot, Photo

import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'disperse-sjl'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def resources(request):
    return render(request, 'resources.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('spot_list')
        else:
            error_message = 'Invalid Signup - Try Again'
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'error': error_message})


def add_photo(request, spot_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            Photo.objects.create(url=url, spot_id=spot_id)
        except Exception as error:
            print('Photo Upload Failed')
            print(error)
    return redirect('spot_detail', pk=spot_id)


class SpotList(LoginRequiredMixin, ListView):
    model = Spot
    fields = '__all__'
    template_name = 'spots/spot_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

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