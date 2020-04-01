from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import Student, Project, MembershipInProject, Coach


class ProjectInline(admin.TabularInline):
    model = Project
    fieldsets = [
        (None, {'fields': ['projectName']})
    ]  # list columns
    extra = 0


class StudentAdmin(admin.ModelAdmin):
    list_display = ('lastName', 'firstName', 'email')
    fields = (('lastName', 'firstName'), 'email')
    inlines = [ProjectInline, ]


admin.site.register(Student, StudentAdmin)


class MembershipInline(admin.StackedInline):
    model = MembershipInProject
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'projectName', 'created_at', 'updated_at', 'projectDuration', 'description', 'isValid', 'creator',
        'total_allocated_by_members')
    fieldsets = (
        ('Etat', {'fields': ('isValid',)}),
        ('A propos', {
            'classes': ('collapse',),
            'fields': ('projectName',  ('creator', 'supervisor'), 'needs', 'description',),
        }),
        ('Durées', {
            'fields': (('projectDuration', 'timeAllocated'),)
        }),
    )
    inlines = (MembershipInline,)


admin.site.register(Project, ProjectAdmin)


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('lastName', 'firstName', 'email')
    fields = (('lastName', 'firstName'), 'email')
