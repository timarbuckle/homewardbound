from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Cat
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def cat_list_view(request):
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'new':
        cats = Cat.objects.filter(status='new')
    elif filter_type == 'adopted':
        time_threshold = timezone.now() - timedelta(hours=24)
        cats = Cat.objects.filter(status='adopted', last_seen__gte=time_threshold)
    else:
        #cats = Cat.objects.all()
        cats = Cat.objects.filter(status='available')

    context = {'cats': cats}

    if request.headers.get('HX-Request'):
        return render(request, 'cats/cat_table.html', context)
    
    return render(request, 'cats/dashboard.html', context)

@require_POST
def update_cats_view(request):
    # This view would trigger the UpdateCats process
    from .updatecats import UpdateCats
    updater = UpdateCats()
    response = updater.update_cats()
    
    # After updating, redirect back to the cat list view
    #return redirect('cat_list')
    context = {
        'total_cats': response['Total'],
        'new_cats': response['New'],
        'adopted_cats': response['Adopted'],
    }

    # 3. RETURN ONLY THE STATS PARTIAL
    return render(request, 'cats/stats_bar.html', context)