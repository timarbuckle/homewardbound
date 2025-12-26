from django.shortcuts import render, redirect
from .models import Cat
from datetime import date

# Create your views here.
def cat_list_view(request):
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'new':
        cats = Cat.objects.filter(first_seen__date__gte=date.today())
    elif filter_type == 'adopted':
        cats = Cat.objects.filter(adopted=True)
    else:
        cats = Cat.objects.all()

    context = {'cats': cats}

    if request.headers.get('HX-Request'):
        return render(request, 'cats/cat_table.html', context)
    
    return render(request, 'cats/dashboard.html', context)

def update_cats_view(request):
    # This view would trigger the UpdateCats process
    from .updatecats import UpdateCats
    updater = UpdateCats()
    updater.update_cats()
    
    # After updating, redirect back to the cat list view
    return redirect('cat_list_view')