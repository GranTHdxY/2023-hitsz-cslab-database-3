from django import forms
from django.forms import formset_factory

class AddressForm(forms.Form):
    address = forms.CharField(label="地址")

class ManageCuisineForm(forms.Form):
    cuisine_name = forms.CharField(label='想要增加的菜品名称')
    cuisine_price = forms.IntegerField(label='菜品价格')
