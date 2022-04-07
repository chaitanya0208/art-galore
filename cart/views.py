from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Artifact, Category
from .cart import Cart

def cart_add(request, artifactid):
	cart = Cart(request)  
	artifact = get_object_or_404(artifact, id=artifactid) 
	cart.add(artifact=artifact)

	return redirect('store:index')

def cart_update(request, artifactid, quantity):
	cart = Cart(request) 
	artifact = get_object_or_404(artifact, id=artifactid) 
	cart.update(artifact=artifact, quantity=quantity)
	price = (artifact.price*quantity)

	return render(request, 'cart/price.html', {"price":price})

def cart_remove(request, artifactid):
    cart = Cart(request)
    artifact = get_object_or_404(artifact, id=artifactid)
    cart.remove(artifact)
    return redirect('cart:cart_details')

def total_cart(request):
	return render(request, 'cart/totalcart.html')

def cart_summary(request):

	return render(request, 'cart/summary.html')

def cart_details(request):
	cart = Cart(request)
	context = {
		"cart": cart,
	}
	return render(request, 'cart/cart.html', context)

