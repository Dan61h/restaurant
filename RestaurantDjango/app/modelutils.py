from django.db import connection
from django.db.models import Q;
from decimal import Decimal

from app.models import *

def GetOrderTotalSum(clientOrder):
    with connection.cursor() as cursor:
        sql = """SELECT SUM(food.price * orderedfood.count) AS total
                 FROM orderedfood
                 INNER JOIN food ON food.id = foodid
                 WHERE orderid = %s"""
        cursor.execute(sql, [clientOrder.id])
        row = cursor.fetchone()
        total = Decimal(0) if row[0] is None else row[0]
        return total


# Функция получения заказов в которых есть только готовые блюда
# и которые не были скрыты

def GetReadyAndNotSeenOrders():
    sql = """
    SELECT * FROM clientorder WHERE seen = FALSE AND id IN (
	    SELECT orderid FROM orderedfood WHERE ready = TRUE GROUP BY orderid
	    EXCEPT
	    SELECT orderid FROM orderedfood WHERE ready = FALSE GROUP BY orderid
)"""
    return ClientOrder.objects.raw(sql)


def SearchClients(search):
    q = Q(name__icontains = search)
    q |= Q(surname__icontains = search)
    q |= Q(otch__icontains = search)
    q |= Q(phone__icontains = search)

    return Client.objects.filter(q)