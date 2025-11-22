
from django.shortcuts import render, HttpResponse
from src.logger import log_error, log_info

# Create your views here.

def contact_form(request):
    try:
        if request.method == "POST":
            data = request.body
            return HttpResponse(content=data)
        
        
    except Exception as e:
        return HttpResponse({"error": e})