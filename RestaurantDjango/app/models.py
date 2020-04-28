"""
Definition of models.
"""

from django.db import models

class Client(models.Model):
    name = models.CharField(max_length = 100)
    surname = models.CharField(max_length = 100)
    otch = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 50)

    class Meta:
        managed = False
        db_table = "client"
        ordering = ["-id"]


class ClientOrder(models.Model):
    date = models.DateTimeField()
    clientid = models.ForeignKey(Client, models.CASCADE, db_column = 'clientid')
    comment = models.CharField(max_length = 200)
    seen = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'clientorder'


class Measure(models.Model):
    name = models.CharField(max_length = 10)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'measure'
        ordering = ["id"]


class Food(models.Model):
    name = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    portionsize = models.IntegerField()
    measureid = models.ForeignKey(Measure, models.SET_NULL, db_column = 'measureid', null = True)
    description = models.CharField(max_length = 500)

    class Meta:
        managed = False
        db_table = 'food'


class OrderedFood(models.Model):
    orderid = models.ForeignKey(ClientOrder, models.DO_NOTHING, db_column = 'orderid')
    foodid = models.ForeignKey(Food, models.CASCADE, db_column = 'foodid')
    ready = models.BooleanField(default = False)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'orderedfood'
        ordering = ["id"]
