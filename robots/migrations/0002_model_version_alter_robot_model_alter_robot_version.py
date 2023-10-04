# Generated by Django 4.2.5 on 2023-10-03 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robots.model')),
            ],
        ),
        migrations.AlterField(
            model_name='robot',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robots.model'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robots.version'),
        ),
    ]
