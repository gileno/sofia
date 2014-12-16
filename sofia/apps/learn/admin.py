from django.contrib import admin

from suit.admin import SortableModelAdmin

from .models import (
    Area, Project, Enrollment, Announcement, Module, Lesson, Material
)


class AreaAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'created', 'modified']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}


class ProjectAdmin(admin.ModelAdmin):

    list_display = ['name', 'leader', 'level', 'created', 'modified']
    search_fields = ['name', 'leader__name', 'description']
    list_filter = ['level']
    prepopulated_fields = {'slug': ['name']}


class EnrollmentAdmin(admin.ModelAdmin):

    list_display = ['user', 'project', 'is_staff', 'created', 'modified']
    search_fields = ['project__name', 'user__name']


class AnnouncementAdmin(admin.ModelAdmin):

    list_display = [
        'title', 'project', 'fixed', 'created_by', 'created', 'modified'
    ]
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title', 'text']
    list_filter = ['project']


class ModuleAdmin(SortableModelAdmin):

    list_display = ['name', 'project', 'order', 'created', 'modified']
    search_fields = ['name', 'project__name', 'description']
    sortable = 'order'
    prepopulated_fields = {'slug': ['name']}
    list_filter = ['project']


class MaterialInline(admin.StackedInline):

    model = Material
    extra = 1


class LessonAdmin(SortableModelAdmin):

    list_display = ['name', 'module', 'order', 'created', 'modified']
    search_fields = ['name', 'module__name', 'description']
    sortable = 'order'
    prepopulated_fields = {'slug': ['name']}
    inlines = [
        MaterialInline,
    ]


class MaterialAdmin(SortableModelAdmin):

    list_display = [
        'name', 'lesson', 'material_type', 'order', 'created', 'modified'
    ]
    search_fields = ['name', 'lesson__name']
    sortable = 'order'


admin.site.register(Area, AreaAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Material, MaterialAdmin)
