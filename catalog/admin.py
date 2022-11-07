from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.

# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)


class BookInline(admin.TabularInline):
    """BookInline"""
    model = Book
    extra = 0  # No Book instances created but shows button to add instance.


class AuthorAdmin(admin.ModelAdmin):
    """AuthorAdmin"""
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]


class BookInstanceInline(admin.TabularInline):
    """"BookInstanceInline"""
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """BookAdmin"""
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """BookInstanceAdmin"""
    list_display = ('book_info', 'due_back', 'borrower', 'status', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
