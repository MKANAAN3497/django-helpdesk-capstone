from django import forms
from .models import Ticket, Comment, Attachment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','description','status','priority','category','assigned_to']

class UserTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','description','category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']
