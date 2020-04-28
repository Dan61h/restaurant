from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from app.models import *
from app.forms import *

import app.utils as utils
import app.modelutils as modelutils

CLIENTS_PER_PAGE = 8
ORDERS_PER_PAGE = 8

def AddNewClient(request):
    if len(request.POST) > 0:
        form = ClientForm(request.POST)
        
        if form.is_valid():
            newClient = Client(**form.cleaned_data)
            newClient.save()
            return HttpResponseRedirect("/clients")
        else:
            context = request.POST.dict()
            context["error"] = utils.GetFormSingleError(form)
            return render(request, "addClient.html", context)
    else:
        return render(request, "addClient.html")


def AllClients(request):
    searchForm = SearchForm(request.GET)

    if searchForm.is_valid():
        searchStr = searchForm.cleaned_data["search"]
        clients = modelutils.SearchClients(searchStr)
        return utils.RenderWithPaging(request, "clientsSearchResults.html", { "search": searchStr }, clients, CLIENTS_PER_PAGE)
    else:
        clients = Client.objects.all()
        return utils.RenderWithPaging(request, "clients.html", dict(), clients, CLIENTS_PER_PAGE)


def ViewClient(request, **kw):
    clientId = kw["clientId"]
    client = get_object_or_404(Client, id = clientId)

    orders = ClientOrder.objects.filter(clientid = clientId).order_by("-date")
    context = { "client": client, "orders": orders }
    return utils.RenderWithPaging(request, "viewClient.html", context, orders, ORDERS_PER_PAGE)


def EditClient(request, **kw):
    clientId = kw["clientId"]
    client = get_object_or_404(Client, id = clientId)

    if len(request.POST) > 0:
        form = ClientForm(request.POST)

        if form.is_valid():
            utils.SetModelFromDict(client, form.cleaned_data)
            client.save()
            return HttpResponseRedirect("/clients/{}".format(clientId))
        else:
            context = request.POST.dict()
            context["error"] = utils.GetFormSingleError(form)
            return render(request, "editClient.html", context)
    else:
        context = dict(client.__dict__)
        return render(request, "editClient.html", context)


def DeleteClient(request):
    try:
        idToDelete = request.GET["id"]
        Client.objects.filter(id = idToDelete).delete()
    except:
        return HttpResponseBadRequest()

    return HttpResponseRedirect("/clients")