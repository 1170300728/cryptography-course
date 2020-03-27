# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('Account', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('Sqe', models.CharField(max_length=20)),
                ('Nickname', models.CharField(max_length=20, blank=True)),
                ('Gender', models.CharField(max_length=10, blank=True)),
                ('Age', models.IntegerField(null=True, blank=True)),
                ('Activecode', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Order', models.CharField(max_length=5)),
                ('Name', models.CharField(max_length=30)),
                ('Phone', models.CharField(max_length=15)),
                ('Postcode', models.CharField(max_length=6, blank=True)),
                ('Province', models.CharField(max_length=30)),
                ('City', models.CharField(max_length=30)),
                ('Address', models.CharField(max_length=50)),
                ('Status', models.CharField(max_length=20)),
                ('Account', models.ForeignKey(to='Eshop.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('SN', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('Date', models.DateTimeField()),
                ('Status', models.CharField(max_length=20)),
                ('Account', models.ForeignKey(to='Eshop.Account')),
                ('Address', models.ForeignKey(to='Eshop.Address')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Priceofone', models.IntegerField()),
                ('Num', models.IntegerField()),
                ('Fororder', models.ForeignKey(to='Eshop.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('Salenum', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('Salename', models.CharField(max_length=50)),
                ('Price', models.DecimalField(max_digits=6, decimal_places=0)),
                ('Numofstore', models.DecimalField(max_digits=6, decimal_places=0)),
                ('Acountformoney', models.CharField(max_length=20)),
                ('Status', models.CharField(max_length=20)),
                ('Eatordrink', models.CharField(max_length=30, blank=True)),
                ('Type', models.CharField(max_length=30, blank=True)),
                ('Pro_place', models.CharField(max_length=30, blank=True)),
                ('Brand', models.CharField(max_length=30, blank=True)),
                ('Weight', models.CharField(max_length=30, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shoppingcar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Num', models.IntegerField()),
                ('Account', models.ForeignKey(to='Eshop.Account')),
                ('Sale', models.ForeignKey(to='Eshop.Sale')),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='Sale',
            field=models.ForeignKey(to='Eshop.Sale'),
        ),
    ]
