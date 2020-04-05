from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.InterviewSlot)
admin.site.register(models.Interview)
admin.site.register(models.InterviewCalendar)
admin.site.register(models.InterviewConflict)