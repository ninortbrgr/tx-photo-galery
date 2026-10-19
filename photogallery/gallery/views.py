from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Gallery

@login_required
def gallery_list_view(request):
    # Check User
    user = request.user
    
    # If the user is a superuser, show all galleries
    if user.is_superuser:
        galleries = Gallery.objects.all()
    else:
        # Filter galleries based on the groups the user belongs to
        user_groups = user.groups.all()
        galleries = Gallery.objects.filter(allowed_groups__in=user_groups).distinct()

    context = {
        'galleries': galleries
    }
    return render(request, 'index.html', context)