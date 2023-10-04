import os
import json
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.shortcuts import get_object_or_404

from orders.models import Order
from .validators import validate_robot_data
from .models import Robot, Model, Version
from .utils import create_production_list, get_difference_datetime_from_today, notify_customers


@csrf_exempt
@require_http_methods(['POST'])
def create_robot(request):
    data = json.loads(request.body)
    if validate_robot_data(data):

        #Создаем робота
        model = get_object_or_404(Model, name=data['model'])
        version = get_object_or_404(Version, name=data['version'], model=model)
        created = data['created']
        robot = Robot.objects.create(serial=f'{data["model"]}-{data["version"]}', model=model, version=version, created=created)

        # Уведомляем покупателей о наличии
        orders = Order.objects.filter(robot_serial=robot.serial, is_notified=False)
        if orders:
            customer_emails = [order.customer.email for order in orders]
            notify_customers(emails=customer_emails, robot_model=robot.model, robot_version=robot.version)
            orders.update(is_notified=True)

        return JsonResponse({'data': robot.to_dict()}, status=HTTPStatus.CREATED)
    return JsonResponse({'message': 'Полученные данные не соотвествуют ожиданиям'}, status=HTTPStatus.BAD_REQUEST)


@require_http_methods(['GET'])
def download_production_list(request):
    robots = Robot.objects.filter(
        created__date__gte=get_difference_datetime_from_today(7)
    ).values('model__name', 'version__name').annotate(robot_count=Count('id'))
    prod_list = create_production_list(robots)

    if os.path.exists(prod_list):
        with open(prod_list, 'rb') as fh:
            response = HttpResponse(
                fh.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=production_list.xlsx'
        return response
    return Http404
