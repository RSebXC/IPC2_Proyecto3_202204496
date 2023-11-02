from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests


def myform_view(request):
    if request.method == 'POST':
        filemensaje = request.FILES.get("file_mensaje")
        fileconfig = request.FILES.get("file_config")

        if not filemensaje or not fileconfig:
            return JsonResponse({"message": "Ambos archivos deben ser cargados."})

        try:
            filesmensaje = {"file": (filemensaje.name, filemensaje.read())}
            responsemensaje = requests.post('http://127.0.0.1:5000/grabarMensajes', files=filesmensaje)
            responsemensaje.raise_for_status()

            filesconfig = {"file": (fileconfig.name, fileconfig.read())}
            responseconfig = requests.post('http://127.0.0.1:5000/grabarConfiguracion', files=filesconfig)
            responseconfig.raise_for_status()

            response_data = {
                "mensaje_response": responsemensaje.json(),
                "config_response": responseconfig.json()
            }

            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)

    return render(request, 'index.html')

def get_Hashtags(request):
    try:
        response = requests.get('http://127.0.0.1:5000/devolverHashtags')
        response.raise_for_status()
        response_data = response.json()
        return JsonResponse(response_data)
    except requests.exceptions.RequestException as e:
        return HttpResponse(str(e), status=500)

def get_feel(request):
    try:
        response = requests.get('http://127.0.0.1:5000/devolverSentimientos')
        response.raise_for_status()
        response_data = response.json()
        return JsonResponse(response_data)
    except requests.exceptions.RequestException as e:
        return HttpResponse(str(e), status=500)

def get_Menciones(request):
    try:
        fecha_inicio = request.GET.get('inicio')
        fecha_fin = request.GET.get('fin')
        opcion = request.GET.get('opcion')
        response = requests.get(f'http://127.0.0.1:5000/devolverDatos/{opcion}?inicio={fecha_inicio}&fin={fecha_fin}')
        response.raise_for_status()
        response_data = response.json()
        return JsonResponse(response_data)
    except requests.exceptions.RequestException as e:
        return HttpResponse(str(e), status=500)
    



