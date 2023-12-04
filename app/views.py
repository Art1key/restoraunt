from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from .forms import DessertForm
from .models import Dish, Ingredient, Order, RecipeEquipment
from .forms import MeatDishesWithOvenForm
from django.http import HttpResponse
from .forms import IngredientForm

def index(request):
    return render(request, 'index.html') #returns the index.html template
def desserts_without_equipment(request):
    form = DessertForm()
    
    return render(request, 'desserts_without_equipment.html', {'form': form})
def show_dish_details(request):
    if request.method == 'POST':
        form = DessertForm(request.POST)
        if form.is_valid():
            dish_id = form.cleaned_data['name'].id
            try:
                dish = Dish.objects.get(id=dish_id)
                return render(request, 'dish_details.html', {'dish': dish})
            except Dish.DoesNotExist:
                return render(request, 'dish_not_found.html')
    else:
        form = DessertForm()

    return render(request, 'desserts_without_equipment.html', {'form': form})
def meat_dishes_with_oven(request):
    if request.method == 'POST':
        form = MeatDishesWithOvenForm(request.POST)
        if form.is_valid():
            selected_dish = form.cleaned_data['meat_dishes']
            # Действия с выбранным блюдом
    else:
        form = MeatDishesWithOvenForm()
    
    return render(request, 'meat_dishes_with_oven.html', {'form': form})

def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'dish_list.html', {'dishes': dishes})
#views.py
from django.shortcuts import render
from .forms import SearchForm
from .models import Dish, Season, Type

def search_dishes(request):
    form = SearchForm(request.POST or None)

    if form.is_valid():
        ingredients = form.cleaned_data.get('ingredients')
        seasons = form.cleaned_data.get('seasons')
        types = form.cleaned_data.get('types')
        equipment = form.cleaned_data.get('equipment')
        queryset = Dish.objects.all()

        if not ingredients or '' in ingredients:
            ingredients = Ingredient.objects.values_list('id', flat=True)

        if not seasons or '' in seasons:
            seasons = Season.objects.all()

        if not types or '' in types:
            types = Type.objects.all()

        if not equipment or '' in equipment:
            equipment = RecipeEquipment.objects.all()

        queryset = queryset.filter(order__name__in=ingredients).distinct()
        queryset = queryset.filter(season__in=seasons)
        queryset = queryset.filter(type__in=types)
        queryset = queryset.filter(equip__in=equipment)

        context = {'form': form, 'dishes': queryset}
        return render(request, 'search_dishes.html', context)

    context = {'form': form}
    return render(request, 'search_dishes.html', context)





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Ingredient
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredient
from .forms import IngredientForm, DishForm
from django.contrib.admin.views.decorators import staff_member_required

def ingredient_edit(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list_admin')
    else:
        form = IngredientForm(instance=ingredient)
    
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'ingredient_edit_admin.html', {'form': form})
    else:
        return render(request, 'ingredient_list.html', {'form': form})

def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient_list.html', {'ingredients': ingredients})

def ingredient_list_admin(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient_list_admin.html', {'ingredients': ingredients})

def bluds_edit(request, dish_id):
    dish = get_object_or_404(Dish, pk=dish_id)
    
    if request.method == 'POST':
        form = DishForm(request.POST, instance=dish)
        if form.is_valid():
            form.save()
            return redirect('bluds_list_admin')
    else:
        form = DishForm(instance=dish)
    
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'bluds_edit.html', {'form': form})
    else:
        return render(request, 'bluds_list.html', {'form': form})

def bluds_list(request):
    dishes = Dish.objects.all()
    return render(request, 'bluds_list.html', {'dishes': dishes})

def bluds_list_admin(request):
    dishes = Dish.objects.all()
    return render(request, 'bluds_list_admin.html', {'dishes': dishes})

def delete(request, dish_id):
    dishes = get_object_or_404(Dish, pk=dish_id)

    if request.method == 'POST':
        dishes.delete()
        return redirect('bluds_list_admin')

    return render(request, 'delete.html', {'dishes': dishes})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Order

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.delete()
        return redirect('bluds_list_admin')

    context = {'order': order}
    return render(request, 'delete_order.html', context)
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User

class AddUserView(View):
    def get(self, request):
        return render(request, 'add_user.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Создание нового пользователя и сохранение его в базе данных
        user = User.objects.create_user(username=username, password=password)
        
        # Дополнительная логика сохранения пользователя в базу данных
        # ...
        
        return redirect('manage_permissions')  # Замените 'manage_permissions' на ваш URL-шаблон
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
class DeleteUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        # Обработка удаления пользователя
        user.delete()
        
        return redirect('manage_permissions')





