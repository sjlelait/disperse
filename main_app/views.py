from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SpotForm
from .models import Spot, Photo

import uuid
import boto3
import os
import requests
import datetime

S3_BASE_URL = "https://s3.us-east-2.amazonaws.com/"
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
            spot = Spot.objects.get(id=spot_id)
            photo = Photo.objects.create(spot=spot, url=url)
            print(f"Image uploaded to S3 and saved to Spot object with URL: {url}")
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_key = os.getenv('API_KEY')
        zip_code = self.object.zipcode
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={zip_code}&days=3&aqi=no&alerts=no"
        response = requests.get(url)
        data = response.json()

    # extract the forecast data for the next 5 days
        forecast = []
        for day in data["forecast"]["forecastday"]:
            forecast_day = {}
            forecast_day["date"] = datetime.datetime.strptime(day["date"], "%Y-%m-%d")
            forecast_day["icon"] = day["day"]["condition"]["icon"]
            forecast_day["condition"] = day["day"]["condition"]["text"]
            forecast_day["high"] = day["day"]["maxtemp_f"]
            forecast_day["low"] = day["day"]["mintemp_f"]
            forecast_day["sunrise"] = day["astro"]["sunrise"]
            forecast_day["sunset"] = day["astro"]["sunset"]
            forecast.append(forecast_day)

        context['forecast'] = data['forecast']['forecastday']
        return context

        

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
    form_class = SpotForm
    template_name = 'spots/spot_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)