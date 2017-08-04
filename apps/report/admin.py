from django.contrib import admin

from .models import Report
from .models import ReportType

# Register your models here.

admin.site.register(Report)
admin.site.register(ReportType)
