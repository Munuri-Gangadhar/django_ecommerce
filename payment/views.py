from django.shortcuts import render,redirect
from cart.cart import Cart
from . forms import ShippingForm,PaymentForm
from . models import ShippingAddress
from django.contrib import messages
# Create your views here.
def payment_success(request):
    return render(request,'payment/payment_success.html',{})

def checkout(request):
    cart=Cart(request)
    cart_products=cart.get_prods
    quantities=cart.get_quants
    totals=cart.cart_total()
    
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.filter(user=request.user).first()
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request,"payment/checkout.html",{"cart_products":cart_products,"quantities":quantities,'totals':totals,"shipping_form":shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request,"payment/checkout.html",{"cart_products":cart_products,"quantities":quantities,'totals':totals,"shipping_form":shipping_form})


def billing_info(request):
    if request.POST:
        cart=Cart(request)
        cart_products=cart.get_prods
        quantities=cart.get_quants
        totals=cart.cart_total()
        shipping_form=request.POST
        my_shipping=request.POST
        request.session['my_shipping']=my_shipping
        
        if request.user.is_authenticated:
            billing_form=PaymentForm()
            return render(request,'payment/billing_info.html',{"cart_products":cart_products,"quantities":quantities,'totals':totals,"shipping_info":request.POST,"billing_form":billing_form})
        else:
            billing_form=PaymentForm()  
            return render(request,'payment/billing_info.html',{"cart_products":cart_products,"quantities":quantities,'totals':totals,"shipping_info":request.POST,"billing_form":billing_form})
    else:
        messages.success(request,"Access denied")
        return redirect('home')


def process_order(request):
    if request.POST:
        payment_form=PaymentForm(request.POST or None)
        my_shipping=request.session.get('my_shipping')
        
        shipping_address=f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"



        messages.success(request,"Order Placed")
        return redirect('home')

    else:
        messages.success(request,"Access Denied")
        return redirect('home')
