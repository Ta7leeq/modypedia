from django.urls import path
from .views import item_list,memory,details

urlpatterns = [
    path('', item_list, name='item_list'),
    path('memory/', memory, name='memory'),
    path('details/<int:item_id>/', details, name='details'),
    
    # Add other paths as needed
]
