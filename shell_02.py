from interface.models import Item
from django.db.models import Q

search_text = "Vermögensschäden"

items = Item.objects.filter(Q(content__icontains=search_text))

print("Total items found:", items.count())
for item in items:
    branch_name = item.branch.branch_name if item.branch else "No Branch"
    print("Branch:", repr(branch_name))
    print("titel:", repr(item.title))
    print("Content:", repr(item.content))
    print("-" * 40)
