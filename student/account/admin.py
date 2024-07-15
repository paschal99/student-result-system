from django.contrib import admin
from .models import Program, Student, Subject, Grade, Marks

# Admin class for Program
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # Display the ID and name in the admin list view
    search_fields = ['name']       # Allow search by program name

# Admin class for Student
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'sex', 'program']  # Display these fields
    search_fields = ['first_name', 'last_name']  # Allow search by first and last name
    list_filter = ['sex', 'program']  # Add filters for sex and program

# Admin class for Subject
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject_code']  # Display ID, name, and subject code
    search_fields = ['name', 'subject_code']  # Allow search by name or subject code

# Admin class for Grade
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # Display ID and grade name
    search_fields = ['name']       # Allow search by grade name

# Admin class for Marks
class MarksAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'subject', 'marks', 'grade']  # Display these fields
    search_fields = ['student__first_name', 'student__last_name', 'subject__name']  # Search by related fields
    list_filter = ['grade', 'subject']  # Add filters for grade and subject

# Register the models with their admin classes
admin.site.register(Program, ProgramAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Marks, MarksAdmin)
