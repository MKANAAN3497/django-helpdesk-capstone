from django.contrib import admin
from .models import Category, Ticket
admin.site.register(Category)
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id','title','status','priority','category','created_by','assigned_to','updated_at')
    list_filter = ('status','priority','category')
    search_fields = ('title','description','created_by__username','assigned_to__username')
