from __future__ import annotations

from django.shortcuts import render

from .models import GalleryImage


def gallery_page(request):
    images = GalleryImage.objects.filter(is_published=True).order_by("-created_at")[:200]
    return render(request, "gallery/gallery.html", {"images": images})

