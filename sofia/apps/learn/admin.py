from django.contrib import admin

from suit.admin import SortableModelAdmin

from .models import Project, Enrollment, Module, Lesson, Material


class ProjectAdmin(admin.ModelAdmin):

    list_display = ['name', 'leader', 'level', 'created', 'modified']
    search_fields = ['name', 'leader__name', 'description']
    list_filter = ['level']
    prepopulated_fields = {'slug': ['name']}


class EnrollmentAdmin(admin.ModelAdmin):

    list_display = ['user', 'project', 'is_staff', 'created', 'modified']
    search_fields = ['project__name', 'user__name']


class ModuleAdmin(SortableModelAdmin):

    list_display = ['name', 'project', 'order', 'created', 'modified']
    search_fields = ['name', 'project__name', 'description']
    sortable = 'order'
    prepopulated_fields = {'slug': ['name']}


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


admin.site.register(Project, ProjectAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Material, MaterialAdmin)
