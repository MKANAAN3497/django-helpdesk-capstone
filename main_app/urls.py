from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),

    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/new/', views.ticket_create, name='ticket_create'),
    path('tickets/<int:id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:id>/edit/', views.ticket_update, name='ticket_update'),
    path('tickets/<int:id>/delete/', views.ticket_delete, name='ticket_delete'),
]
