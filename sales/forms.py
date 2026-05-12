from django import forms
from .models import Order

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = [
            'full_name',
            'email',
            'product',
            'quantity',
            'price',
            'status'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg px-4 py-2'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'w-full border rounded-lg px-4 py-2'
            }),

            'product': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg px-4 py-2'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'w-full border rounded-lg px-4 py-2'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'w-full border rounded-lg px-4 py-2'
            }),

            'status': forms.Select(attrs={
                'class': 'w-full border rounded-lg px-4 py-2'
            }),
        }