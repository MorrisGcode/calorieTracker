from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from datetime import date
from .models import FoodItem
from .forms import FoodItemForm

def register_view(request):
    '''
    user Registration
    '''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('calorie_tracker')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    '''
    user login
    '''
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('calorie_tracker')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def calorie_tracker_view(request):
    '''
    total amount of calories taken 
    '''
    today = date.today()
    food_items_today = FoodItem.objects.filter(user=request.user, date_added=today).order_by('-id')
    total_calories = sum(item.calories for item in food_items_today)

    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.user = request.user
            food_item.save()
            return redirect('calorie_tracker')
    else:
        form = FoodItemForm()

    context = {
        'food_items': food_items_today,
        'total_calories': total_calories,
        'form': form,
    }
    return render(request, 'calorie_tracker.html', context)

@login_required
def remove_food_item(request, item_id):
    '''
    remove food items already input
    '''
    item = get_object_or_404(FoodItem, id=item_id, user=request.user)
    if request.method == 'POST': 
        item.delete()
    return redirect('calorie_tracker')

@login_required
def reset_calories(request):
    '''
    Resets calories to start over
    '''
    today = date.today()
    if request.method == 'POST':
        FoodItem.objects.filter(user=request.user, date_added=today).delete()
    return redirect('calorie_tracker')