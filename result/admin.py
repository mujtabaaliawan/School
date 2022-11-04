from django.contrib import admin
from result.models import Result

print("yo")

class ResultAdmin(admin.ModelAdmin):
    fieldsets = [
        ('student_data', {'fields': ['student']}),
        ('student_result', {'fields': ['course', 'score']})
    ]


admin.site.register(Result, ResultAdmin)
