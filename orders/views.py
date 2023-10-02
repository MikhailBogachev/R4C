from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .forms import OrderForm
from .models import Order
from customers.models import Customer


@csrf_exempt
@require_http_methods(['POST'])
def create_order(request):
    form = OrderForm(request.POST)
    form_data = form.data
    if form.is_valid():
        customer, _ = Customer.objects.get_or_create(
            email=form_data['email']
        )
        Order.objects.create(
            customer=customer,
            robot_serial=form_data['robot_serial']
        )
    return HttpResponse('Ваш заказ принят!')
