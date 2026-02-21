from django.shortcuts import render
from django.http import JsonResponse
from .models import ProjectDemo
from src.logger import log_error
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt 


# ---------- Common paginator utility ----------
def paginator(page_no: int) -> dict:
    """
    Returns 9 records per page
    """
    try:
        qs = ProjectDemo.objects.filter(is_active=True).order_by("-uploaded_at")

        paginator = Paginator(qs, 9)  # 9 per page

        if page_no > paginator.num_pages:
            return {}

        page = paginator.page(page_no)

        data = []
        for obj in page.object_list:
            data.append({
                "title": obj.title,
                "thumbnail": obj.thumbnail.file.url if obj.thumbnail else None,
                "project_path": obj.project_path
            })

        return {
            "page": page_no,
            "has_next": page.has_next(),
            "has_prev": page.has_previous(),
            "total_pages": paginator.num_pages,
            "results": data
        }

    except Exception as e:
        log_error(
            f"Paginator Error\n"
            f"Exception: {type(e).__name__}\n"
            f"Message: {e}"
        )
        return {}


# ---------- Initial Page Load ----------
@csrf_exempt
def project_view(request):
    try:
        data = paginator(1)  # first 9 records

        return render(request, "projects.html", {
            "projects": data.get("results", []),
            "page_data": data
        })
       # return JsonResponse({"data":data}, status=200)

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


# ---------- Pagination API ----------
@csrf_exempt
def project_pagination(request, id):
    """
    id = page number
    """
    try:
        data = paginator(id)

        if not data:
            return JsonResponse({"data": {}}, status=200)

        return JsonResponse({"data": data}, status=200)

    except Exception as e:
        log_error(
            f"Error occurred while rendering portfolio (project) pagination view.\n"
            f"Exception: {type(e).__name__}\n"
            f"Message: {e}"
        )

        return JsonResponse({"error": "Pagination failed"}, status=500)


# ---------- Filter API ----------
@csrf_exempt
def project_pagination_filter(request, filter):
    """
    filter = category string (Business, Portfolio, Blog, E-Commerce, Landing-Page)
    """
    try:
        qs = ProjectDemo.objects.filter(
            is_active=True,
            category=filter
        ).order_by("-uploaded_at")[:9]

        data = []

        for obj in qs:
            data.append({
                "title": obj.title,
                "thumbnail": obj.thumbnail.file.url if obj.thumbnail else None,
                "project_path": obj.project_path
            })

        return JsonResponse({
            "filter": filter,
            "count": len(data),
            "results": data
        }, status=200)

    except Exception as e:
        log_error(
            f"Error occurred while rendering portfolio (project) pagination filter view.\n"
            f"Exception: {type(e).__name__}\n"
            f"Message: {e}"
        )

        return JsonResponse({"error": "Filter failed"}, status=500)