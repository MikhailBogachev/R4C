import json
from http import HTTPStatus
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# from .forms import RobotForm
from .validators import validate_robot_data
from .models import Robot


@csrf_exempt
@require_http_methods(['POST'])
def create_robot(request):
    data = json.loads(request.body)
    if validate_robot_data(data):
        robot = Robot.objects.create(**data)
        return JsonResponse({'data': robot.to_dict()}, status=HTTPStatus.CREATED)
    return JsonResponse({'message': 'Не удалось сохранить данные'}, status=HTTPStatus.BAD_REQUEST)
