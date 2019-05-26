from django.contrib import admin

from catalog.models import Author, Genre, Language, Book, BookInstance


class BookInline(admin.TabularInline):
    model = Book
    extra = 0 # zero inlines


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    #exclude = ('last_name',)

    inlines = [BookInline]


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower','due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        #('Details', {
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
