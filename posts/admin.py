from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_at', 'views', 'is_published', 'created_at')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at',)
