import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modypedia.settings")
django.setup()

from interface.models import Item, Field

# Get the field (case-insensitive)
field_obj = Field.objects.filter(field_name__iexact="Fachkundeprüfung").first()

if not field_obj:
    print("❌ Field 'Fachkundeprüfung' not found!")
    exit()

# Filter items with this field
items = Item.objects.filter(field=field_obj)

print("🔧 Found", items.count(), "items. Setting next_time = None...")

# Update each item's next_time to None
for item in items:
    item.next_time = None
    item.save()

print("✅ next_time successfully set to None for all matching items.")
