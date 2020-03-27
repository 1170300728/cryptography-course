from django.db import models
from django.contrib import admin
from django.contrib.admin.models import LogEntry


# Create your models here.
class Account(models.Model):
    Account = models.CharField(max_length=30, primary_key=True)
    Sqe = models.CharField(max_length=20)
    Nickname = models.CharField(max_length=20, blank=True)
    Gender = models.CharField(max_length=10, blank=True)
    Age = models.IntegerField(null=True, blank=True)
    Activecode = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.Account


class Address(models.Model):
    Account = models.ForeignKey(Account,on_delete=models.CASCADE)
    Order = models.CharField(max_length=5)
    Name = models.CharField(max_length=30)
    Phone = models.CharField(max_length=15)
    Postcode = models.CharField(max_length=6, blank=True)
    Province = models.CharField(max_length=30)
    City = models.CharField(max_length=30)
    Address = models.CharField(max_length=50)
    Status = models.CharField(max_length=20)

    def __unicode__(self):
        return self.Address


class Sale(models.Model):
    Salenum = models.CharField(max_length=10, primary_key=True)
    Salename = models.CharField(max_length=50)
    Price = models.DecimalField(max_digits=6, decimal_places=0)
    Numofstore = models.DecimalField(max_digits=6, decimal_places=0)
    Acountformoney = models.CharField(max_length=20)
    Status = models.CharField(max_length=20)

    Type = models.CharField(max_length=30, blank=True)
    Pro_place = models.CharField(max_length=30, blank=True)
    Size = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.Salename


class Shoppingcar(models.Model):
    Account = models.ForeignKey(Account,on_delete=models.CASCADE)
    Sale = models.ForeignKey(Sale,on_delete=models.CASCADE)
    Num = models.IntegerField()

    def __unicode__(self):
        return self.Account.Account


class Order(models.Model):
    Account = models.ForeignKey(Account,on_delete=models.CASCADE)
    SN = models.CharField(max_length=20, primary_key=True)
    Date = models.DateTimeField()
    Status = models.CharField(max_length=20)
    Address = models.ForeignKey(Address,on_delete=models.CASCADE)

    def __unicode__(self):
        return self.SN


class OrderItem(models.Model):
    Sale = models.ForeignKey(Sale,on_delete=models.CASCADE)
    Fororder = models.ForeignKey(Order,on_delete=models.CASCADE)
    Priceofone = models.IntegerField()
    Num = models.IntegerField()

    def __unicode__(self):
        return self.Sale.Salenum


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = [
        'action_time', 'user', 'content_type', 'object_id',
        'object_repr', 'action_flag', 'change_message', 'objects']


class Pass(models.Model):
    Dual = models.CharField(max_length=255, default='')
