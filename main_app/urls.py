from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resources/', views.resources, name='resources'),
    path('spots/', views.SpotList.as_view(), name='spot_list'),
    path('spots/<int:pk>/', views.SpotDetail.as_view(), name='spot_detail'),
    path('spots/<int:pk>/update/', views.SpotUpdate.as_view(), name='spot_update'),
    path('spots/<int:pk>/delete/', views.SpotDelete.as_view(), name='spot_delete'),
    path('spots/create/', views.SpotCreate.as_view(), name='spot_create'),
    path('accounts/signup/', views.signup, name='signup'),
    path('spots/<int:spot_id>/add_photo/', views.add_photo, name='add_photo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)