from django.contrib import admin, messages

# Register your models here.
from .models import Project


class ProjectInline(admin.TabularInline):
    model = Project
    fieldsets = [
        (None, {'fields': ['project_name']})
    ]  # list columns
    extra = 0


class ProjetDureeListFilter(admin.SimpleListFilter):
    title = 'duration'
    parameter_name = 'duration'

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
            messages.error(request, "%s projects valid= false" %
                           rows_NValid.count())
        else:
            rows_updated = queryset.update(isValid=False)
            if rows_updated == 1:
                message = "1 project was"
            else:
                message = "%s projects were" % rows_updated
            self.message_user(request, level='success',
                              message="%s successfully marked as not valid" % message)

    set_to_Nvalid.short_description = "Refuser"
    actions = [set_Valid, 'set_to_Nvalid']

    list_display = (
        'project_name', 'created_at', 'updated_at', 'duration',
        'description', 'is_valid', 'creator')
    fieldsets = (
        ('Etat', {'fields': ('is_valid',)}),
        ('A propos', {
            'classes': ('collapse',),
            'fields': ('project_name',  'creator', 'needs', 'description',),
        }),
        ('Durées', {
            'fields': (('duration', 'allocated_time'),)
        }),
    )
    actions_on_bottom = True
    actions_on_top = False


admin.site.register(Project, ProjectAdmin)
