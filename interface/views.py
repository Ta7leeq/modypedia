
from django.shortcuts import render, redirect
from .models import Item
from .forms import ItemFilterForm
from datetime import date, timedelta,datetime
from django.forms.models import model_to_dict

def item_list(request):
    form = ItemFilterForm(request.GET)
    items = Item.objects.all()

    if form.is_valid():
        if form.cleaned_data['item_type']:
            items = items.filter(item_type=form.cleaned_data['item_type'])
        if form.cleaned_data['title']:
            items = items.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['author']:
            items = items.filter(author__icontains=form.cleaned_data['author'])
        if form.cleaned_data['date_created_from']:
            items = items.filter(date_created__gte=form.cleaned_data['date_created_from'])
        if form.cleaned_data['date_created_to']:
            items = items.filter(date_created__lte=form.cleaned_data['date_created_to'])
        if form.cleaned_data['tags']:
            tags = form.cleaned_data['tags'].split(',')
            for tag in tags:
                items = items.filter(tags__icontains=tag.strip())

    return render(request, 'interface/item_list.html', {'form': form, 'items': items})

def memory(request):
    if request.method == 'POST':
        
        if 'delete' in request.POST:
            post_id=request.POST.get('delete')
            delete_item = Item.objects.get(id=post_id)
            delete_item.delete()
        
        elif 'reset' in request.POST:
            post_id=request.POST.get('reset')
            reset_item = Item.objects.get(id=post_id)
            reset_item.next_time=reset_date().date()
            reset_item.save()
            return redirect('memory')
        
        elif 'done' in request.POST:
            post_id=request.POST.get('done')
            done_item = Item.objects.get(id=post_id)
            
            
            done_item.next_time=calculate_next_time(done_item.last_time,done_item.next_time)
            done_item.save()
            return redirect('memory')
            
    

        
    form = ItemFilterForm(request.GET)
    items = Item.objects.filter(next_time__lte=date.today())
    

    if form.is_valid():
        if form.cleaned_data['item_type']:
            items = items.filter(item_type=form.cleaned_data['item_type'])
        if form.cleaned_data['title']:
            items = items.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['author']:
            items = items.filter(author__icontains=form.cleaned_data['author'])
        if form.cleaned_data['date_created_from']:
            items = items.filter(date_created__gte=form.cleaned_data['date_created_from'])
        if form.cleaned_data['date_created_to']:
            items = items.filter(date_created__lte=form.cleaned_data['date_created_to'])
        if form.cleaned_data['tags']:
            tags = form.cleaned_data['tags'].split(',')
            for tag in tags:
                items = items.filter(tags__icontains=tag.strip())

    return render(request, 'interface/today_list.html', {'form': form, 'items': items})






def calculate_next_time(last_time, next_time):
    # Calculate the current interval in days between last_time and next_time
    current_interval = (next_time - last_time).days

    # Initialize the next Fibonacci interval
    if current_interval == 0:
        next_interval = 1  # Start from 1 if the interval is zero (initial case)
    elif current_interval == 1:
        next_interval = 2  # Start with the second Fibonacci number
    else:
        # Apply the Fibonacci sequence by calculating the next interval
        prev_interval = current_interval
        next_interval = current_interval + prev_interval
    
    # Cap the interval at 90 days (approximately 3 months)
    max_interval = 90
    if next_interval > max_interval:
        next_interval = max_interval

    # Calculate the next review time by adding the interval in days
    next_time = last_time + timedelta(days=next_interval)

    return next_time

def reset_date():
    next_time=datetime.now()+timedelta(days=1)
    return next_time