from django import forms

from .models import Order


class OrderForm(forms.Form):
    email = forms.EmailField()
    robot_serial = forms.CharField(max_length=5)
