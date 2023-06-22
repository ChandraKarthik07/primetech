from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse 
from search.models import Dish,Item
import pandas as pd
from django.db.models import Q,F

def search_view(request):
    query = request.GET.get('query')
    if query:
        items = Item.objects.filter(name__icontains=query).order_by('price')
        dishes = Dish.objects.filter(items__in=items).distinct()
        if not dishes:
            query = "No results found. Showing all dishes."
            dishes = Dish.objects.all().order_by('items__price', '-restaurant_name')
    else:
        dishes = Dish.objects.all().order_by('items__price', '-restaurant_name')[:10]
    
    # Group items by dish and restaurant
    grouped_dishes = {}
    for dish in dishes:
        items = dish.items.all().order_by('price')
        if dish.restaurant_name in grouped_dishes:
            grouped_dishes[dish.restaurant_name].append((dish, items))
        else:
            grouped_dishes[dish.restaurant_name] = [(dish, items)]
    
    return render(request, 'index.html', {'grouped_dishes': grouped_dishes, 'query': query})



# def fill_models_from_csv(request):
#     data = pd.read_csv(r"C:\Users\Karthik\Downloads\restaurants_small.csv")

#     # Iterate over the rows and create Dish model instances
#     for index, row in data.iterrows():
#         id = row['id']
#         restaurant_name = row['name']
#         items = row['items']
#         location = row['location']

#         # Create a Dish instance and save it
#         dish = Dish.objects.create(id=id, restaurant_name=restaurant_name, items=items, location=location)

#     return HttpResponse("Successfully inserted data from CSV file.")

def fill_models_from_csv(request):
    data = pd.read_csv(r"C:\Users\Karthik\Downloads\restaurants_small.csv")
    
    for index, row in data.iterrows():
        dish_id = int(row['id'])
        restaurant_name = row['name']
        location = row['location']
        items_data = row['items']
        
        # Create Dish instance
        dish, created = Dish.objects.get_or_create(id=dish_id, restaurant_name=restaurant_name, location=location)
        
        # Process items data and create/update Item instances
        items = process_items_data(items_data)
        
        for item_data in items:
            item_name = item_data['name']
            item_price = item_data['price']
            
            # Create or update Item instance
            item, created = Item.objects.get_or_create(name=item_name, defaults={'price': item_price})
            
            # Add the Item to the Dish
            dish.items.add(item)
        
    return JsonResponse({'message': 'Data inserted successfully.'})

def process_items_data(items_data):
    items = []
    items_data = items_data.strip()  # Remove leading/trailing spaces
    
    # Split the items data by comma
    items_list = items_data.split(',')
    
    for item in items_list:
        item = item.strip()  # Remove leading/trailing spaces
        print(f"Processing item: {item}")
        
        # Split the item data by colon
        item_data = item.split(':')
        
        if len(item_data) == 2:
            item_name = item_data[0].strip()
            item_price = item_data[1].strip()
            print(f"Item name: {item_name}, Item price: {item_price}")
            
            items.append({'name': item_name, 'price': item_price})
    
    return items


