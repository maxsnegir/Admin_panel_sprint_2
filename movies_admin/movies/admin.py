from django.contrib import admin
from .models import FilmWork, Person, Genre


class PersonRoleInline(admin.TabularInline):
    model = FilmWork.person.through
    extra = 0


class GenreFilmWorkInline(admin.TabularInline):
    model = FilmWork.genres.through
    extra = 0


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):

    list_display = ('title', 'type', 'creation_date', 'rating',)
    fields = ('title', 'type', 'description', 'creation_date', 'certificate', 'file_path', 'rating',)
    ordering = ('title', 'creation_date')
    search_fields = ('title',)
    inlines = [GenreFilmWorkInline, PersonRoleInline, ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )
    exclude = ("id",)
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    exclude = ("id", )
    list_display = ('full_name', 'birth_date')
    search_fields = ('full_name', )
    ordering = ('full_name', 'birth_date')
    inlines = [PersonRoleInline, ]
