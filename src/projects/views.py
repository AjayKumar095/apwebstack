from django.shortcuts import render
from .models import ProjectDemo
from src.logger import log_error

# Create your views here.
def paginator(page_no:int)->dict:
    pass 

def project_view(request):
    try:
        return render(request, "projects.html")
    except Exception as e:
        context = {
            "status": 404,
            "error": "Page Not Found",
            "message": "Sorry, the page you are looking for doesn’t exist or may have been moved.",
            "page": "portfolio"
        }

        log_error(
            f"Error occurred while rendering portfolio (project) page.\n"
            f"Exception: {type(e).__name__}\n"
            f"Message: {e}"
        )

        return render(
            request=request,
            template_name="error/errors.html",
            context=context,
            status=404
        )
        
def project_pagination(request):
    
    try:
        pass
    except Exception as e:
        context = {
            "status": 404,
            "error": "Page Not Found",
            "message": "Sorry, the page you are looking for doesn’t exist or may have been moved.",
            "page": "portfolio"
        }

        log_error(
            f"Error occurred while rendering portfolio (project) pagination view.\n"
            f"Exception: {type(e).__name__}\n"
            f"Message: {e}"
        )

        return render(
            request=request,
            template_name="error/errors.html",
            context=context,
            status=404
        )    