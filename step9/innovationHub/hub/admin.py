from django.contrib import admin, messages

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
    search_fields = ['lastName', 'firstName']
    inlines = [ProjectInline, ]


admin.site.register(Student, StudentAdmin)


class MembershipInline(admin.StackedInline):
    model = MembershipInProject
    extra = 1


class ProjetDureeListFilter(admin.SimpleListFilter):
    title = 'Duree'
    parameter_name = 'duree'

    def lookups(self, request, model_admin):
        return (
            ('1 mois', ("moins d'un mois")),
            ('3 mois', ("Plus que 1 mois"))
        )

    def queryset(self, request, queryset):
        if self.value() == '1 mois':
            return queryset.filter(projectDuration__lte=30)
        if self.value() == '3 mois':
            return queryset.filter(projectDuration__lte=90, projectDuration__gte=30)


def set_Valid(modeladmin, request, queryset):
    queryset.update(isValid=True)


set_Valid.short_description = "Valider"


class ProjectAdmin(admin.ModelAdmin):

    def set_to_Nvalid(self, request, queryset):
        rows_NValid = queryset.filter(isValid=False)
        if rows_NValid.count() > 0:
            messages.error(request, "%s projects valid= false" % rows_NValid.count())
        else:
            rows_updated = queryset.update(isValid=False)
            if rows_updated == 1:
                message = "1 project was"
            else:
                message = "%s projects were" % rows_updated
            self.message_user(request, level='success', message="%s successfully marked as not valid" % message)

    set_to_Nvalid.short_description = "Refuser"
    actions = [set_Valid, 'set_to_Nvalid']

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
    list_filter = ('creator', 'isValid', ProjetDureeListFilter)
    list_per_page = 1
    actions_on_bottom = True
    actions_on_top = False


admin.site.register(Project, ProjectAdmin)


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('lastName', 'firstName', 'email')
    fields = (('lastName', 'firstName'), 'email')
    ordering = ['firstName']
