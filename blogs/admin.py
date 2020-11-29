from django.contrib import admin

# Register your models here.
from .models import BlogPost

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_on')
    search_fields = ['title', 'content']


admin.site.register(BlogPost, PostAdmin)
