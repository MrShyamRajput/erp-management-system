from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer, Order, OrderItem

from .forms import OrderForm, OrderItemForm
def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        item_form = OrderItemForm(request.POST)

        if order_form.is_valid() and item_form.is_valid():

            # get customer data
            full_name = order_form.cleaned_data['full_name']
            email = order_form.cleaned_data['email']

            # create or get customer
            customer, created = Customer.objects.get_or_create(
                email=email,
                defaults={"full_name": full_name}
            )

            # create order
            order = order_form.save(commit=False)
            order.customer = customer
            order.save()

            # create order item
            item = item_form.save(commit=False)
            item.order = order
            item.save()

            messages.success(request, "Order Created Successfully")
            return redirect('create_order')

        else:
            print(order_form.errors)
            print(item_form.errors)
            messages.error(request, "Form Error")
            return redirect('create_order')

    # GET request
    order_form = OrderForm()
    item_form = OrderItemForm()

    return render(request, 'sales.html', {
        "order_form": order_form,
        "item_form": item_form,
        "products":Product.objects.all()
        
    })