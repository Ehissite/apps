from django.shortcuts import render, redirect
from item.models import Category, Item

from .forms import SignupForm


# Create your views here.
def home(request):
    items = Item.objects.filter(is_sold=False) [0:6]
    categories = Category.objects.all()
    return render(request, 'core/home.html', {
        'items':items, 
        'categories':categories})

def contact(request):
    return render(request, 'core/contact.html', {})

def signup(request):
    # checking the request method is set to post
    if request.method == "POST":
        form = SignupForm(request.POST)
        # validating the form
        if form.is_valid():
            # saving the form if its valid
            form.save()
            # redirecting the user to the login page
            return redirect('/login')
    else:
        form = SignupForm()
    
    return render(request, 'core/signup.html', {
        'form':form
    })

def login(request):
    return render(request, 'core/login.html', {})