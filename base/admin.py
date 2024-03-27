from django.contrib import admin
from . models import User,Topic,Room,Message
# Register your models here.

admin.site.register(User)
admin.site.register(Topic)
class send(admin.StackedInline):
    model= Message
    extra = 0

class RoomAdmin(admin.ModelAdmin):
    inlines=[
        send
    ]
admin.site.register(Room,RoomAdmin)
