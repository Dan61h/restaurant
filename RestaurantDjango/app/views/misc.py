from django.shortcuts import render

def MainPage(request):
    return render(request, "mainPage.html")