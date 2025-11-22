from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from src.logger import log_error, log_info
from .models import ContactForm


# ------------------ CONTACT PAGE VIEW ------------------
def contact(request):
    try:
        # Read response data coming from redirect
        msg_type = request.GET.get("type")   # success, error, warning
        message = request.GET.get("msg")     # the actual message text

        context = {
            "msg_type": msg_type,
            "message": message,
        }

        return render(request, 'contact.html', context)

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

# ------------------ CONTACT FORM SUBMIT VIEW ------------------
def contact_form(request):
    try:
        if request.method != "POST":
            return redirect(
                f"{reverse('contact')}?type=warning&msg=Invalid request method"
            )

        # Get form data
        first = request.POST.get("first_name")
        last = request.POST.get("last_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Basic validation
        if not first or not email or not message:
            return redirect(
                f"{reverse('contact')}?type=error&msg=All required fields must be filled"
            )

        # Save to database
        ContactForm.objects.create(
            first_name=first,
            last_name=last,
            email=email,
            message=message,
        )

        # SUCCESS redirect
        return redirect(
            f"{reverse('contact')}?type=success&msg=Thank you for contacting us!"
        )

    except Exception as e:
        log_error(f"Error in contact form submit: {e}")
        return redirect(
            f"{reverse('contact')}?type=error&msg=Something went wrong while submitting the form"
        )
