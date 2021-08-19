from django.contrib import admin
from django.contrib.admin import ModelAdmin

from main.models import *


class HostelImageInLine(admin.TabularInline):
    model = HostelImage
    max_num = 10
    min_num = 1


@admin.register(Hostel)
class PostAdmin(admin.ModelAdmin):
    inlines = [HostelImageInLine]


admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Rating)

