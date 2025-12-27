from django.shortcuts import render, redirect
from django.urls import reverse
from src.logger import log_error
from .models import Contact_Form, Contact_Meta


# ------------------ CONTACT PAGE VIEW ------------------
def contact(request):
    try:
        # Read response data coming from redirect
        msg_type = request.GET.get("type")   # success, error, warning
        message = request.GET.get("msg")     # the actual message text
        
        meta = Contact_Meta.objects.first()
        
        context = {
        "msg_type": msg_type,
        "message": message,

        # Meta fields
        "meta_title": meta.meta_title if meta else "",
        "meta_description": meta.meta_description if meta else "",
        "meta_keywords": meta.meta_keywords if meta else "",
        "canonical_url": meta.canonical_url if meta else "",

        "og_title": meta.og_title if meta else "",
        "og_description": meta.og_description if meta else "",
        "og_image": meta.og_image.url if meta and meta.og_image else "",

        "twitter_title": meta.twitter_title if meta else "",
        "twitter_description": meta.twitter_description if meta else "",
        "twitter_image": meta.twitter_image.url if meta and meta.twitter_image else "",

        "no_index": meta.no_index if meta else False,
        "no_follow": meta.no_follow if meta else False,
    }

        return render(request, 'contact.html', context)

    except Exception as e:
        context = {
            "status": 404,
            "error": "Page Not Found",
            "message": "Sorry, the page you are looking for doesn’t exist or may have been moved.",
            "page": "contact"
        }

        log_error(
            f"Error occurred while rendering contact page.\n"
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
        Contact_Form.objects.create(
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
