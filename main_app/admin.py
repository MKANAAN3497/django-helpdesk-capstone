from django.contrib import admin
from .models import Ticket, Category, Comment, Attachment

admin.site.register(Ticket)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Attachment)
