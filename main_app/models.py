from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    TYPES = [
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('network', 'Network'),
        ('security', 'Security'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=80, unique=True)
    type = models.CharField(max_length=30, choices=TYPES, default='other')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Ticket(models.Model):
    PRIORITY = [('low','Low'),('medium','Medium'),('high','High'),('urgent','Urgent')]
    STATUS = [('open','Open'),('in_progress','In Progress'),('on_hold','On Hold'),('resolved','Resolved'),('closed','Closed')]

    title = models.CharField(max_length=160)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY, default='medium')
    status = models.CharField(max_length=20, choices=STATUS, default='open')
    due_date = models.DateField(null=True, blank=True)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_created')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tickets_assigned')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at','-created_at']

    def __str__(self): return f"#{self.pk} {self.title}"
