from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from django.urls import reverse
from .models import Reservation
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm
from .forms import ServiceForm 
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date

login_required
def index(request):
    if request.user.is_staff:
        if request.user.is_superuser:
            # Load admin panel for superusers
            return render(request, 'admin/index.html')
        else:
            # Load staff panel for staff members
            return render(request, 'staff/index.html')
    elif request.user.is_authenticated:
        # Load user panel for regular users
        return render(request, 'user/index.html')
    else:
        # Load guest panel for unauthenticated users
        return render(request, 'guest/index.html')



def services(request):
  return render(request, 'services.html')


def redirect_to_homepage(request):
  return render(request, 'landingpage.html')

def reservation_list(request):
    all_reservations = Reservation.objects.all()
    all_transactions = Transaction.objects.all()
    pending_reservations = all_reservations.filter(status='pending')
    approved_reservations = all_reservations.filter(status='approved')
    declined_reservations = all_reservations.filter(status='declined')

    template = loader.get_template('admin/reservation_list.html')
    context = {
        'all_reservations': all_reservations,
        'pending_reservations': pending_reservations,
        'approved_reservations': approved_reservations,
        'declined_reservations': declined_reservations,
        'all_transactions': all_transactions,
    }

    return HttpResponse(template.render(context, request))



def payments_list(request):
    reservations = Reservation.objects.all()
    template = loader.get_template('admin/payment_list.html')
    context = {
        'reservations': reservations,
    }

    return HttpResponse(template.render(context, request))

def reservation_form(request, id):
    service = Services.objects.get(id=id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  # Set the current user as the reservation's user
            reservation.service = service  

            # Check if there's already a reservation for the selected date
            existing_reservation = Reservation.objects.filter(date=reservation.date).exists()
            if existing_reservation:
                messages.error(request, 'Sorry, this date is already reserved. Please try other dates.')
                return redirect('reservation:reservation_form', id=id)

            reservation.save()
            return redirect('/user_reservation_list/')
    else:
        form = ReservationForm()
    return render(request, 'reservation_form.html', {'form': form, 'service_name': service.service_name, 'service_price': service.price})


def payment_form(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    return render(request, 'payment_form.html', {'reservation': reservation})


def customers(request):
    users = User.objects.all()
    
    context = {
        'users': users,
    }

    return render(request, 'admin/customer_list.html', context)
    

def reserve_service(request, service_id):
   
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date = request.POST.get('date')
        phone_number = request.POST.get('phone_number')
           
        service = Services.objects.get(id=service_id)

        reservation = Reservation.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            date=date,
            phone_number=phone_number,
            service=service,
            status='pending'
        )
        return redirect('service_detail', service_id=service_id)
    else:
        

        pass
       
def services_list(request):
    service = Services.objects.all()
    template = loader.get_template('blog/index.html')
    context = {
        'services' : service,
    }
    return HttpResponse(template.render(context, request))

def transactions(request):
    service = Services.objects.all()
    template = loader.get_template('admin/transactions.html')
    context = {
        'services' : service,
    }
    return HttpResponse(template.render(context, request))

def services_list_admin(request):
    service = Services.objects.all()
    template = loader.get_template('admin/services.html')
    context = {
        'services' : service,
    }
    return HttpResponse(template.render(context, request))

    
def update_status(request, id):
    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            reservation = Reservation.objects.get(id=id)
            reservation.status = status
            reservation.save()
        except Reservation.DoesNotExist:
            pass  
    return redirect('reservation:reservation_list')

def user_reservation_list(request):
    user = request.user
    pending_reservations = Reservation.objects.filter(user=user, status='pending')
    declined_reservations = Reservation.objects.filter(user=user, status='declined')
    approved_reservations = Reservation.objects.filter(user=user, status='approved')
    

    transactions = Transaction.objects.filter(reservation__user=user)
    
    return render(request, 'reservation_history.html', {
        'pending_reservations': pending_reservations,
        'declined_reservations': declined_reservations,
        'approved_reservations': approved_reservations,
        
        'transactions': transactions,
    })

def user_transaction_list(request):
    user = request.user
    pending_reservations = Reservation.objects.filter(user=user, status='pending')
    declined_reservations = Reservation.objects.filter(user=user, status='declined')
    approved_reservations = Reservation.objects.filter(user=user, status='approved')
    

    transactions = Transaction.objects.filter(reservation__user=user)
    
    return render(request, 'transaction_list.html', {
        'pending_reservations': pending_reservations,
        'declined_reservations': declined_reservations,
        'approved_reservations': approved_reservations,
        
        'transactions': transactions,
    })





def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/services/')
    else:
        form = ServiceForm()
    return render(request, 'admin/add_service.html', {'form': form})

def update_service(request, id):
    service = get_object_or_404(Services, id=id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/services/')  # Redirect to the services list page
    else:
        form = ServiceForm(instance=service)
    return render(request, 'admin/update_service.html', {'form': form})

def report_list_admin(request):
    # Fetch counts
    total_users = User.objects.count()
    total_reservations = Reservation.objects.count()
    total_packages = Services.objects.count()
    total_transactions = Transaction.objects.count()
    approved_count = Reservation.objects.filter(status='Approved').count()
    declined_count = Reservation.objects.filter(status='Declined').count()
    pending_count = Reservation.objects.filter(status='Pending').count()

    # Handle date search
    search_date = request.GET.get('date')
    reservations = None
    if search_date:
        search_date = parse_date(search_date)
        if search_date:
            reservations = Reservation.objects.filter(date=search_date)
    
    # Annotate reservations with transaction title and transaction id or default text
    annotated_reservations = []
    if reservations:
        for reservation in reservations:
            transaction = reservation.transaction_set.first()
            if transaction:
                transaction_title = transaction.title
                transaction_id = transaction.id
            else:
                transaction_title = "No transaction"
                transaction_id = None
            
            annotated_reservations.append({
                'id': reservation.id,
                'username': reservation.user.username,
                'full_name': f"{reservation.first_name} {reservation.last_name}",
                'phone_number': reservation.phone_number,
                'service': reservation.service.service_name,
                'date': reservation.date,
                'transaction_title': transaction_title,
                'transaction_id': transaction_id,  # Include transaction ID
                'status': reservation.status,
            })

    context = {
        'total_user': total_users,
        'approved_count': approved_count,
        'declined_count': declined_count,
        'pending_count': pending_count,
        'total_reservation': total_reservations,
        'total_package': total_packages,
        'total_transactions' : total_transactions,
        'reservations': annotated_reservations,
        'search_date': search_date,
    }
    return render(request, 'admin/reports.html', context)

def delete_service(request, id):
    service = get_object_or_404(Services, id=id)
    if request.method == 'POST':
        service.delete()
        return redirect('/services/')  # Redirect to the services list page
    return render(request, 'admin/delete_service.html', {'service': service})

def todos1(request, id):    
    if request.method == 'POST':
        try:
            
            data = json.loads(request.body)
            transaction_id = data.get('transaction_id')
            amount = data.get('amount')
            date = data.get('date')
            
            
            if not transaction_id or not amount or not date:
                return JsonResponse({"error": "Missing transaction_id, amount, or date"}, status=400)
            
            
            reservation = get_object_or_404(Reservation, id=id)
            
            
            transaction = Transaction.objects.create(
                title=transaction_id,
                amount=amount,
                date=date,
                reservation=reservation  
            )
            transaction.save()
            return JsonResponse({"message": "Transaction details saved successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "GET method not allowed"}, status=405)
    

def transaction_history(request):
    transactions = Transaction.objects.all()
    return render(request, 'admin/transactions.html', {'transactions': transactions})

def done_payment(request):
  return render(request, 'done_payment.html')