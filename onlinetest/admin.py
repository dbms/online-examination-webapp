from django.contrib import admin

from .models import clientsTable, studentProfile, question, quesFile, studentMark
# Register your models here.
admin.site.register(clientsTable)
admin.site.register(studentProfile)
admin.site.register(question)
admin.site.register(quesFile)
admin.site.register(studentMark)

