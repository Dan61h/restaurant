from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from app.models import *
from app.forms import *

import app.utils as utils

FOOD_PER_PAGE = 8

def RenderEditFoodPage(request, template, context = dict()):
    measures = Measure.objects.all()
    context["measures"] = measures
    return render(request, template, context)


def AllFood(request):
    allFood = Food.objects.all().select_related("measureid").order_by("name")
    return utils.RenderWithPaging(request, "food.html", dict(), allFood, FOOD_PER_PAGE)


def AddNewFood(request):
    if len(request.POST) > 0:
        form = FoodForm(request.POST)

        if form.is_valid():
            newFood = Food(**form.cleaned_data)
            newFood.save()
            return HttpResponseRedirect("/food")
        else:
            context = request.POST.dict()
            context["error"] = utils.GetFormSingleError(form)
            return RenderEditFoodPage(request, "addFood.html", context)
    else:
        return RenderEditFoodPage(request, "addFood.html")


def EditFood(request, **kw):
    foodId = kw["foodId"]
    food = get_object_or_404(Food, id = foodId)

    if len(request.POST) > 0:
        form = FoodForm(request.POST)

        if form.is_valid():
            utils.SetModelFromDict(food, form.cleaned_data)
            food.save()
            return HttpResponseRedirect("/food")
        else:
            context = request.POST.dict()
            context["error"] = utils.GetFormSingleError(form)
            return RenderEditFoodPage(request, "editFood.html", context)
    else:
        context = dict(food.__dict__)
        context["measureid"] = str(context["measureid_id"])
        return RenderEditFoodPage(request, "editFood.html", context)


def DeleteFood(request, **kw):
    try:
        idToDelete = request.GET["id"]
        Food.objects.filter(id = idToDelete).delete()
    except:
        return HttpResponseBadRequest()

    return HttpResponseRedirect("/food")