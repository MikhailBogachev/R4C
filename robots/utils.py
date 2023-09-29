import xlsxwriter
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import os


def create_production_list(robots):
    dict_robots = {}
    for robot in robots:
        dict_robots[robot['model']] = dict_robots.get(robot['model'], []) + [robot]

    workbook = xlsxwriter.Workbook('production_list/demo.xlsx')
    workbook.set_properties({'encoding': 'utf-8'})
    for model, list_models in dict_robots.items():
        worksheet = workbook.add_worksheet(name=model)
        worksheet.write(0, 0, 'Модель')
        worksheet.write(0, 1, 'Версия')
        worksheet.write(0, 2, 'Количество за неделю')
        for ind, robot in enumerate(list_models):
            worksheet.write(ind+1, 0, robot['model'])
            worksheet.write(ind+1, 1, robot['version'])
            worksheet.write(ind+1, 2, robot['model_count'])
    workbook.close()

    return os.path.join(settings.BASE_DIR, 'production_list/demo.xlsx')


def get_difference_datetime_from_today(days: int):
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    return some_day_last_week
