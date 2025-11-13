from django.shortcuts import render


def index(request):
    site = {
        "title": "apwebstack",
        "heading": "Web development service",
        "subheading": "This is sub heading"
    }

    return render(request,"index.html", {"site": site})

    