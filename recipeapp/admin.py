from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Recipe, Comment


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    list_filter = ('status', 'date_created', 'approved', 'category')
    search_fields = ['title', 'about', 'method', 'ingredients__item',
                     'category']
    list_display = ('title', 'date_updated', 'status', 'date_created',
                    'approved')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('about', 'method', 'nutrition', 'ingredients')
    actions = ['approve_recipes']

    def approve_recipes(self, queryset):
        queryset.update(approved=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ('approved',)
    search_fields = ['name', 'email', 'message']
    list_display = ('name', 'message', 'recipe', 'date_posted', 'approved')
    summernote_fields = ('message')

    actions = ['approve_comments']

    def approve_comments(self, queryset):
        queryset.update(approved=True)
