from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

admin.site.register(models.Commonuser)
admin.site.register(models.Accountuser)
admin.site.register(models.Superuser)