from django.contrib import admin
from .models import Term, Specialty, Group, Student, Subject, SubjectInstance, Lecturer, Task, Mark

# Register your models here.

admin.site.register(Term)
admin.site.register(Specialty)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(SubjectInstance)
admin.site.register(Lecturer)
admin.site.register(Task)
admin.site.register(Mark)
