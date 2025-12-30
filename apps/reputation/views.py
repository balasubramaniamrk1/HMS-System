from django.shortcuts import render
from .models import Review

def public_reviews(request):
    """
    Display a list of featured reviews for the public.
    """
    # Fetch only featured reviews, ordered by date (newest first)
    reviews = Review.objects.filter(is_featured=True).order_by('-review_date')
    
    return render(request, 'reputation/review_list.html', {
        'reviews': reviews
    })
