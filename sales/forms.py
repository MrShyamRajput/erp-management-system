from django import forms
from .models import Order, OrderItem

class OrderForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = Order
        fields = ['status']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']