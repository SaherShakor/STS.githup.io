from django.contrib import admin
from sts import models as usermodels 

class Test(admin.ModelAdmin):
    list_display = ('email','user_type',)
admin.site.register(usermodels.User, Test)
admin.site.register(usermodels.Trip)
admin.site.register(usermodels.Captain)