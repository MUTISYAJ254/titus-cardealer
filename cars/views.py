from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, CarImage
from .forms import CarForm, CarImageForm
from django.contrib.auth.decorators import login_required, user_passes_test

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_detail.html', {'car': car})

@login_required
@user_passes_test(lambda user: user.has_perm('cars.add_car'))
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'cars/car_form.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.has_perm('cars.change_car'))
def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/car_form.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.has_perm('cars.delete_car'))
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'cars/car_confirm_delete.html', {'car': car})

@login_required
@user_passes_test(lambda user: user.has_perm('cars.add_carimage'))
def upload_car_image(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        form = CarImageForm(request.POST, request.FILES)
        if form.is_valid():
            car_image = form.save(commit=False)
            car_image.car = car
            car_image.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarImageForm(initial={'car': car})
    return render(request, 'cars/upload_car_image.html', {'form': form, 'car': car})
