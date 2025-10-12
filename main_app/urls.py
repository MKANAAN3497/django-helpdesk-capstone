from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),

    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/new/', views.ticket_create, name='ticket_create'),
    path('tickets/<int:id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:id>/edit/', views.ticket_update, name='ticket_update'),
    path('tickets/<int:id>/delete/', views.ticket_delete, name='ticket_delete'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
]
