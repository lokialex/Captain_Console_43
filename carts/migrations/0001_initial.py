# Generated by Django 3.0.5 on 2020-05-02 19:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('card_number', models.CharField(max_length=10)),
                ('expiration_date', models.DateTimeField()),
                ('cvv', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('address_1', models.CharField(max_length=255)),
                ('address_2', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postcode', models.IntegerField()),
                ('country', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=datetime.date(2020, 5, 2))),
                ('Payment_information_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='carts.PaymentInformation')),
                ('productID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.Product')),
                ('shipping_information_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='carts.ShippingInformation')),
            ],
        ),
    ]