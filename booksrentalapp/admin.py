from django.contrib import admin
from .models import Book, Rent, Category, BookCategory


class BookCategoryInline(admin.StackedInline):
    model = BookCategory
    extra = 1


class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'description',  'pub_date', 'author']}),
    ]
    inlines = [BookCategoryInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Rent)
admin.site.register(Category)
