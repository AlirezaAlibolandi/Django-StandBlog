from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category']
    list_filter = ['tags', 'category']
    search_fields = ['title']
    date_hierarchy = 'updated'
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 50


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(comments)
admin.site.register(Likes)