from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author', 'publication_year')

    # Fields to filter by in the sidebar
    list_filter = ('author', 'publication_year')

    # Fields to search by using the search bar
    search_fields = ('title', 'author')

# Register the model with the custom admin class
admin.site.register(Book, BookAdmin)