from django.shortcuts import render, HttpResponse

# Create your views here.
def service_detail(request):
    return HttpResponse({"service": "Page working perfectly"})