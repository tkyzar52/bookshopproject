from django.contrib import admin
from .models import Book, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title", "description")
    list_filter = ("categories",)
    filter_horizontal = ("categories",) 

    def display_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    display_categories.short_description = "Categories"
