
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('spots/', views.SpotList.as_view(), name='spot_list'),
    path('toys/<int:pk>/', views.SpotDetail.as_view(), name='spot_detail'),
]