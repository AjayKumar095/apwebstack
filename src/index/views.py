from django.shortcuts import render
from src.logger import log_error


def index(request):
    
    try:
        return render(request=request, template_name="index/index.html")
    except Exception as e:
        context = {
            "status": 404,
            "error": "Page Not Found",
            "message": "Sorry, the page you are looking for doesn’t exist or may have been moved.",
            "page": "index"
        }

        log_error(
            f"Error occurred while rendering index page.\n"
            f"Exception: {type(e).__name__}\n"
            f"Message: {e}"
        )

        return render(
            request=request,
            template_name="error/errors.html",
            context=context,
            status=404
        )
