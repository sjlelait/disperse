
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('spots/', views.SpotList.as_view(), name='spot_list'),
    path('spots/<int:pk>/', views.SpotDetail.as_view(), name='spot_detail'),
    path('spots/<int:pk>/update/', views.SpotUpdate.as_view(), name='spot_update'),
    path('spots/<int:pk>/delete/', views.SpotDelete.as_view(), name='spot_delete'),
]