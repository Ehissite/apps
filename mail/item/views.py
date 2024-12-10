# importing decorators to ensure the user is loggedin 
from django.contrib.auth.decorators import login_required
from django.db.models import Q # this makes it possible to search in multiple fields
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from .forms import NewItemForm, EditItemForm

# Create your views here.

def browse(request):
    query = request.GET.get('query', '') # passing a get request method 
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)
    
    # To be able to filter by category
    if category_id:
        items = items.filter(category_id=category_id)
    
    # filter search if there is any query
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query)) # we are filtering/searching for the items found in the query
        
    
    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'title': "Browse",
    })

def detail(request, pk):
    # to get the item from database
    item = get_object_or_404(Item, pk=pk) # django would give an error if this item is not found in the database
    # related items
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    
    return render(request, 'item/detail.html', {
        'item':item,
        'related_items':related_items,
    })
    
@login_required
def new(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user 
            item.save()
            
            return redirect('item:detail', pk=item.id)
    else:    
        form = NewItemForm()
    return render(request, 'item/form.html', {
        'form': form,
        'title': "New Item",
    })
    
    
@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user) # to get the object using the primary key
    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item) # setting the instance to ensure the data on the form is passed
        
        if form.is_valid():
            form.save()
            
            return redirect('item:detail', pk=item.id)
    else:    
        form = EditItemForm(instance=item)
    return render(request, 'item/form.html', {
        'form': form,
        'title': "Edit Item",
    })
    
    
    
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user) # to get the object using the primary key
    item.delete()
    
    return redirect('dashboard:dashboard')