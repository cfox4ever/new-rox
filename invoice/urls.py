from django.urls import path
from . import views
urlpatterns = [
   path('', views.invoice_list, name='invoice_list'),
   path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
   path('recieve_now/<int:pk>/',views.recieve_now,name='recieve_now'),
   path('sent_to_ap_date/<int:pk>/',views.sent_to_ap_date,name='sent_to_ap_date'),
]