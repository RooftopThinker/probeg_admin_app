from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context


@csrf_exempt
def test(request):
    print(request)
    return HttpResponse(200)
