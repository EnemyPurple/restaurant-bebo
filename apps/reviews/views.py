from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import redirect, render

from .models import Review
from .models import ReviewPhoto
from .forms import ReviewCreateForm
from apps.users.models import OperationLog


def reviews_page(request):
    reviews = Review.objects.filter(is_published=True).prefetch_related("photos").order_by("-created_at")
    stats = Review.objects.filter(is_published=True).aggregate(avg_rating=Avg("rating"), total=Count("id"))
    return render(request, "reviews/reviews.html", {"reviews": reviews, "stats": stats})


@login_required
def add_review(request):
    if request.method == "POST":
        form = ReviewCreateForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            review: Review = form.save(commit=False)
            review.user = request.user
            review.name = getattr(getattr(request.user, "profile", None), "full_name", "") or request.user.username
            review.is_published = False
            review.save()

            for f in request.FILES.getlist("photos"):
                ReviewPhoto.objects.create(review=review, image=f)

            OperationLog.objects.create(
                user=request.user,
                kind=OperationLog.Kind.REVIEW_CREATED,
                description=f"Отзыв по брони #{review.booking_id}" if review.booking_id else "Отзыв",
            )
            messages.success(request, "Спасибо! Отзыв отправлен на модерацию.")
            return redirect("users:cabinet")
    else:
        form = ReviewCreateForm(user=request.user)
    return render(request, "reviews/add.html", {"form": form})

