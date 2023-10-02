import os
import json
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

from .validators import validate_robot_data
from .models import Robot
from .utils import create_production_list, get_difference_datetime_from_today


@csrf_exempt
@require_http_methods(['POST'])
def create_robot(request):
    data = json.loads(request.body)
    if validate_robot_data(data):
        data.update({'serial': f'{data["model"]}-{data["version"]}'})
        robot = Robot.objects.create(**data)
        return JsonResponse({'data': robot.to_dict()}, status=HTTPStatus.CREATED)
    return JsonResponse({'message': 'Не удалось сохранить данные'}, status=HTTPStatus.BAD_REQUEST)


@require_http_methods(['GET'])
def download_production_list(request):
    robots = Robot.objects.filter(
        created__date__gte=get_difference_datetime_from_today(7)
    ).values('model', 'version').annotate(model_count=Count('id'))
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
