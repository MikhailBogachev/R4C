import os
from datetime import timedelta

import xlsxwriter
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail


def create_production_list(robots):
    dict_robots = {}
    for robot in robots:
        dict_robots[robot['model__name']] = dict_robots.get(robot['model__name'], []) + [robot]

    workbook = xlsxwriter.Workbook('production_list/robots_list.xlsx')
    workbook.set_properties({'encoding': 'utf-8'})
    for model, list_models in dict_robots.items():
        worksheet = workbook.add_worksheet(name=model)
        worksheet.write(0, 0, 'Модель')
        worksheet.write(0, 1, 'Версия')
        worksheet.write(0, 2, 'Количество за неделю')
        for ind, robot in enumerate(list_models):
            worksheet.write(ind+1, 0, robot['model__name'])
            worksheet.write(ind+1, 1, robot['version__name'])
            worksheet.write(ind+1, 2, robot['robot_count'])
    workbook.close()

    return os.path.join(settings.BASE_DIR, 'production_list/robots_list.xlsx')


def get_difference_datetime_from_today(days: int):
    some_day_last_week = timezone.now().date() - timedelta(days=days)
    return some_day_last_week


def notify_customers(emails, robot_model, robot_version):
    send_mail(
        subject='Робот в наличии!',
        message=
        f"""
            Добрый день!
            Недавно вы интересовались нашим роботом модели {robot_model}, версии {robot_version}.
            Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
        """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=False
    )
