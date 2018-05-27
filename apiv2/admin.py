# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class ReportAdmin(admin.ModelAdmin):
    list_display = ["__unicode__","comment","date_created"]
    list_filter = ["date_created"]
    search_fields = ["comment"]

    class Meta:
        model = Report

# Register your models here.
admin.site.register(ReportRating)
admin.site.register(ReportTag)
admin.site.register(Report,ReportAdmin)
