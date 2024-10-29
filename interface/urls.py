from django.urls import path
from .views import item_list,memory

urlpatterns = [
    path('items/', item_list, name='item_list'),
    path('memory/', memory, name='memory'),
    # Add other paths as needed
]
