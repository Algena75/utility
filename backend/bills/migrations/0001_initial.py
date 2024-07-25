# Generated by Django 5.0.1 on 2024-07-25 05:01

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apartments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('WA', 'Вода'), ('CP', 'Содержание общего имущества')], default='WA', max_length=2, verbose_name='Вид платежа')),
                ('value', models.DecimalField(decimal_places=2, default=1.0, max_digits=7, verbose_name='Тариф')),
                ('from_date', models.DateField(default=datetime.datetime.today, verbose_name='Дата ввода тарифа')),
                ('until_date', models.DateField(null=True, verbose_name='Дата отмены тарифа')),
                ('is_current', models.BooleanField(default=True, verbose_name='Статус тарифа')),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Вода')),
                ('community_property', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Содержание общего имущества')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='ИТОГО')),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='apartments.apartment')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='apartments.period')),
            ],
        ),
    ]
