from django.contrib import admin
from app import models
# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Expense)
admin.site.register(models.Balance)