# Generated by Django 4.2.5 on 2023-10-03 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_unique_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_notified',
            field=models.BooleanField(default=False),
        ),
    ]