from django.contrib import admin

from .models import Topic, Reply


class TopicAdmin(admin.ModelAdmin):

    list_display = [
        'title', 'author', 'content_object', 'views', 'created', 'modified'
    ]
    search_fields = ['title', 'author__email', 'author__name', 'text']
    list_filter = ['created', 'modified']
    prepopulated_fields = {'slug': ['title']}


class ReplyAdmin(admin.ModelAdmin):

    list_display = [
        'topic', 'author', 'right_answer', 'created', 'modified'
    ]
    search_fields = ['topic__title', 'author__email', 'author__name', 'text']
    list_filter = ['right_answer', 'created', 'modified']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Reply, ReplyAdmin)
