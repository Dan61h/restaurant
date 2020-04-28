from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from app.models import *
from app.forms import *

import app.utils as utils
import app.modelutils as modelutils

import datetime

FOOD_PER_PAGE = 8

def NewOrder(request, **kw):
    clientId = kw["clientId"]
    client = get_object_or_404(Client, id = clientId)

    if len(request.POST) > 0:
        form = ClientOrderForm(request.POST)

        if form.is_valid():
            newOrder = ClientOrder(**form.cleaned_data)
            newOrder.clientid = client
            newOrder.date = datetime.datetime.now()
            newOrder.seen = False
            newOrder.save()
            return HttpResponseRedirect("/clients/{}".format(clientId))
        else:
            context = request.POST.dict()
            context["error"] = utils.GetFormSingleError(form)
            return render(request, "addOrder.html", context)
    else:
        context = { "client": client }
        return render(request, "addOrder.html", context)


def EditOrder(request, **kw):
    orderId = kw["orderId"]
    order = get_object_or_404(ClientOrder, id = orderId)

    if len(request.POST) > 0:
        form = ClientOrderForm(request.POST)

        if form.is_valid():
            utils.SetModelFromDict(order, form.cleaned_data)
            order.save()
            return HttpResponseRedirect("/order/{}".format(orderId))
        else:
            context = request.POST.dict()
            context["error"] = utils.GetFormSingleError(form)
            return render(request, "editOrder.html", context)
    else:
        context = dict(order.__dict__)
        return render(request, "editOrder.html", context)


def ViewOrder(request, **kw):
    orderId = kw["orderId"]
    clOrder = get_object_or_404(ClientOrder, id = orderId)

    total = modelutils.GetOrderTotalSum(clOrder)
    client = clOrder.clientid
    orderedFood = OrderedFood.objects.filter(orderid = orderId).select_related("foodid")

    context = {
        "total": total,
        "client": client,
        "order": clOrder,
        "orderedFood": orderedFood
    }
    return render(request, "viewOrder.html", context)


def DeleteOrder(request, **kw):
    try:
        idToDelete = request.GET["id"]
        ClientOrder.objects.filter(id = idToDelete).delete()
    except:
        return HttpResponseBadRequest()

    return HttpResponseRedirect("/clients/{}".format(kw["clientId"]))


def RemoveOrderedFood(request, **kw):
    try:
        oFoodToDeleteId = request.GET["id"]
        OrderedFood.objects.filter(id = oFoodToDeleteId).delete()
    except:
        return HttpResponseBadRequest()

    return HttpResponseRedirect("/order/{}".format(kw["orderId"]))


def AddOrderedFood(request, **kw):
    orderId = kw["orderId"]
    clOrder = get_object_or_404(ClientOrder, id = orderId)
    food = Food.objects.all().select_related("measureid").order_by("name")

    if len(request.POST) > 0:
        form = AddOrderedFoodForm(request.POST)

        if form.is_valid():
            ordFood = OrderedFood(**form.cleaned_data)
            ordFood.orderid = clOrder
            ordFood.ready = False
            ordFood.save()
            return HttpResponseRedirect("/order/{}/addfood".format(orderId))
        else:
            context = {
                "order": clOrder,
                "error": utils.GetFormSingleError(form)
            }
    else:
        context = { "order": clOrder }

    return utils.RenderWithPaging(request, "AddFoodToOrder.html", context, food, FOOD_PER_PAGE)


def MakeReady(request, **kw):
    try:
        toMakeReadyId = request.GET["id"]
        oFood = OrderedFood.objects.get(id = toMakeReadyId)
        oFood.ready = True
        oFood.save()
    except:
        return HttpResponseBadRequest()

    return HttpResponseRedirect("/order/{}".format(kw["orderId"]))


def MakeSeen(request, **kw):
    try:
        toMakeSeenId = request.GET["id"]
        order = ClientOrder.objects.get(id = toMakeSeenId)
        order.seen = True
        order.save()
    except:
        return HttpResponseBadRequest()

    return HttpResponseRedirect("/ready")


def ViewReadyOrders(request):
    readyOrders = modelutils.GetReadyAndNotSeenOrders()
    context = { "readyOrders": readyOrders }
    return render(request, "ready.html", context)