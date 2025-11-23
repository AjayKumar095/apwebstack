from django.shortcuts import render
from src.logger import log_error

# Create your views here.
def terms_of_use(request):
    try:
        return render(request, 'core/termsofuse.html')
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