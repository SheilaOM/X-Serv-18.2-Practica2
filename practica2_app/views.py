from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from practica2_app.models import Urls
from django.views.decorators.csrf import csrf_exempt
import urllib.parse


# Create your views here.

@csrf_exempt
def barra(request):
    lista_urls = Urls.objects.all();
    if request.method == 'GET':
        if Urls.objects.all().exists():
            resp = "Las urls acortadas son:<br/>"
            for url in lista_urls:
                resp += "-/" + str(url.id) + " -> " + url.url_larga + "<br/>"
        else:
            resp = "No hay urls acortadas."

        resp += " Introduce una nueva url para acortar:"
        resp += "<form method='POST' action=''><input type='text'" \
            " name='url_larga'><input type='submit' " \
            "value='Acortar'></form>"

    elif request.method == 'POST':
        url_larga = urllib.parse.unquote(request.POST['url_larga'])
        if (url_larga[0:7] != "http://" and url_larga[0:8] != "https://"):
            url_larga = "http://" + url_larga

        if url_larga in lista_urls:
            url_corta = "/" + url_larga.id
        else:
            url = Urls(url_larga=url_larga)
            url.save()
            url_corta = Urls.objects.get(url_larga=url_larga).id
        resp = "La url acortada de " + url_larga + " es " + str(url_corta)

    return HttpResponse(resp)

def redirect(request, url_corta):
    try:
        url_larga = Urls.objects.get(id=url_corta).url_larga
        return HttpResponseRedirect(url_larga)
    except Urls.DoesNotExist:
        resp = "url no disponible"
        return HttpResponse(resp)

def error(request):
    resp = "url incorrecta, debe ser un dígito"
    return HttpResponse(resp)
