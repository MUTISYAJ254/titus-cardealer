from django import forms
from .models import Car, CarImage

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'color', 'mileage', 'price', 'notes', 'image']

class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['car', 'image']