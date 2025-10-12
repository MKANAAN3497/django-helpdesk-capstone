from django import forms
from .models import Category, Ticket

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'type')

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority', 'status', 'due_date', 'category', 'assigned_to')