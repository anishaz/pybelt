from django.shortcuts import render, redirect
from ..loginreg.models import User
from . models import Product, ProductManager
from django.contrib import messages
from django.core.urlresolvers import reverse

def dashboard(request):
    if not 'user' in request.session:
        return redirect('/main')

    print request.session['user']
    id = request.session['user']
    user = User.objects.get(id=id)

    data = {
        "product" : Product.objects.filter(users=user),
        "other_product" : Product.objects.exclude(users=user)
    }

    print data
    return render(request, 'wishlist/dashboard.html', data)

def create(request):
    return render(request, 'wishlist/create.html')

def add(request):
    data = request.POST.copy()
    data ['id'] = request.session['user']
    result = Product.objects.productValidate(data)

    if 'errors' in result:
        for errors in result['errors']:
            messages.add_message(request, messages.ERROR, errors)
        return redirect('/wish_items/create')

    request.session['product_id'] = result['product'].id

    return redirect('/dashboard')

def delete(request, id):
    product = Product.objects.get(id=id).delete()
    return redirect ('/dashboard')

def mylist(request, id):
    product = Product.objects.get(id=id)
    user = request.session['user']
    person = User.objects.get(id=user)
    product.users.add(person)

    return redirect ('/dashboard')

def remove(request,id):
    product = Product.objects.get(id=id)
    user = request.session['user']
    person = User.objects.get(id=user)
    product.users.remove(person)

    return redirect ('/dashboard')

def view(request, id):
    data = {
        "product" : Product.objects.get(id=id)
    }

    return render(request, 'wishlist/item.html', data)
