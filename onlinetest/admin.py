from django.contrib import admin

from .models import testDetails,studentProfile, question, studentMark, clientsTable
# Register your models here.
admin.site.register(testDetails)
admin.site.register(studentProfile)
admin.site.register(question)
admin.site.register(studentMark)
admin.site.register(clientsTable)


