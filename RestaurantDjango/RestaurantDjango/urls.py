"""
Definition of urls for RestaurantDjango.
"""

from django.urls import path
from django.urls import re_path
from django.conf.urls.static import serve
import django.contrib.auth.views

import RestaurantDjango.settings as settings

import app.views.client
import app.views.food
import app.views.order
import app.views.misc
import app.views.measure

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    path("",                                app.views.misc.MainPage),
    path("clients",                         app.views.client.AllClients),
    path("clients/add",                     app.views.client.AddNewClient),
    path("clients/delete",                  app.views.client.DeleteClient),
    path("clients/<int:clientId>",          app.views.client.ViewClient),
    path("clients/<int:clientId>/edit",     app.views.client.EditClient),
    path("clients/<int:clientId>/neworder", app.views.order.NewOrder),
    path("clients/<int:clientId>/deleteorder", app.views.order.DeleteOrder),
    path("food",                            app.views.food.AllFood),
    path("food/add",                        app.views.food.AddNewFood),
    path("food/delete",                     app.views.food.DeleteFood),
    path("food/<int:foodId>/edit",          app.views.food.EditFood),
    path("order/<int:orderId>",             app.views.order.ViewOrder),
    path("order/<int:orderId>/edit",        app.views.order.EditOrder),
    path("order/<int:orderId>/addfood",     app.views.order.AddOrderedFood),
    path("order/<int:orderId>/removefood",  app.views.order.RemoveOrderedFood),
    path("order/<int:orderId>/makeready",   app.views.order.MakeReady),
    path("measure",                         app.views.measure.AllMeasures),
    path("measure/add",                     app.views.measure.AddMeasure),
    path("measure/<int:measureId>/edit",    app.views.measure.EditMeasure),
    path("measure/delete",                  app.views.measure.DeleteMeasure),
    path("ready",                           app.views.order.ViewReadyOrders),
    path("ready/makeseen",                  app.views.order.MakeSeen)
]

#urlpatterns += [
    #re_path(r'^static/(?P<path>.*)$', serve, { 'document_root': settings.STATIC_ROOT })
#]