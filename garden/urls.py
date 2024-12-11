from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('customer/<int:id>/', views.customer, name='customer'),
    path('logout/', views.logout_view, name='logout'),

    path('customer_reservation_list/', views.customer_reservation_list, name='customer_reservation_list'),
    path('services/', views.services_list_admin, name='services_list_admin'),
    path('services/add_service/', views.add_service, name='add_service'),
    path('services/update_service/<int:id>/', views.update_service, name='update_service'),
    path('customers/', views.customers, name='customers'),
    path('customer/<int:customer_id>/reservation_form/<int:service_id>/', views.reservation_form, name='reservation_form'),
    path('payment_form/<int:id>/', views.payment_form, name='payment_form'),
    path('reservation_list/', views.reservation_list, name='reservation_list'),
    path('home', views.services_list, name='services_list'),
    path('update_status/<int:id>/', views.update_status, name='update_status'), 
    path('reports/', views.report_list_admin, name='report_list_admin'),
    path('services/delete/<int:id>/', views.delete_service, name='delete_service'),
    path('todos1/<int:id>/', views.todos1, name='todos1'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
    path('payment_form/<int:id>done_payment/', views.done_payment, name='done_payment'),
    path('transactions/', views.user_transaction_list, name='user_transaction_list'),
    
]