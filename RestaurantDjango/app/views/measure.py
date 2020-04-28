from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

import app.utils as utils

from app.models import *
from app.forms import *

def AllMeasures(request):
    measures = Measure.objects.all();
    context = { "measures": measures }
    return render(request, "measures.html", context)


def AddMeasure(request):
    form = MeasureForm(request.POST)

    if form.is_valid():
        measure = Measure(**form.cleaned_data)
        measure.save()
        return HttpResponseRedirect("/measure")
    else:
        return HttpResponseRedirect("/measure")


def EditMeasure(request, **kw):
    measure = get_object_or_404(Measure, id = kw["measureId"])
    form = MeasureForm(request.POST)

    if form.is_valid():
        utils.SetModelFromDict(measure, form.cleaned_data)
        measure.save()
        return HttpResponseRedirect("/measure")
    else:
        return HttpResponseRedirect("/measure")

def DeleteMeasure(request):
    try:
        idToDelete = request.GET["id"]
        Measure.objects.filter(id = idToDelete).delete()
    except:
        return HttpResponseBadRequest()

    return HttpResponseRedirect("/measure")