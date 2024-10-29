from django.contrib import admin
from .models import Item, Tag, ItemTag, Relationship,Domain,Field,Branch,Area,Topic,Section,Aspect

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_type', 'author', 'date_created')
    search_fields = ('title', 'author', 'tags')
    list_filter = ('item_type', 'date_created')
    fieldsets = (
        (None, {
            'fields': ('item_type', 'title', 'content', 'author','platform','domain','field','branch','area','topic','section','aspect','tags','link','last_time','next_time')
        }),
        ('Dates', {
            'fields': ('date_created',),
        }),
    )
    readonly_fields = ('date_created',)

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain_name',)
    search_fields = ('domain_name',)

@admin.register(Field)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('field_name',)
    search_fields = ('field_name',)

@admin.register(Branch)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('branch_name',)
    search_fields = ('branch_name',)

@admin.register(Area)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('area_name',)
    search_fields = ('area_name',)

@admin.register(Topic)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('topic_name',)
    search_fields = ('topic_name',)

@admin.register(Section)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('section_name',)
    search_fields = ('section_name',)

@admin.register(Aspect)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('aspect_name',)
    search_fields = ('aspect_name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)
    search_fields = ('tag_name',)

@admin.register(ItemTag)
class ItemTagAdmin(admin.ModelAdmin):
    list_display = ('item', 'tag')
    search_fields = ('item__title', 'tag__tag_name')
    autocomplete_fields = ('item', 'tag')

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('item1', 'item2', 'relationship_type')
    search_fields = ('item1__title', 'item2__title', 'relationship_type')
    autocomplete_fields = ('item1', 'item2')
    list_filter = ('relationship_type',)
