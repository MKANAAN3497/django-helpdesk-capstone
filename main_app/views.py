from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Ticket, Category, Comment, Attachment
from .forms import TicketForm, UserTicketForm, CommentForm, AttachmentForm

class Home(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    my_open = Ticket.objects.filter(created_by=request.user, status='open').count()
    assigned_to_me = Ticket.objects.filter(assigned_to=request.user).exclude(status__in=['resolved','closed']).count()
    resolved = Ticket.objects.filter(created_by=request.user, status='resolved').count()
    return render(request, 'dashboard.html', {'my_open': my_open, 'assigned_to_me': assigned_to_me, 'resolved': resolved})

@login_required
def ticket_list(request):
    if request.user.is_superuser:
        qs = Ticket.objects.select_related('created_by','assigned_to','category')
    elif request.user.is_staff:
        qs = Ticket.objects.select_related('created_by','assigned_to','category').filter(assigned_to=request.user)
    else:
        qs = Ticket.objects.select_related('created_by','assigned_to','category').filter(created_by=request.user)
    status = request.GET.get('status') or ''
    priority = request.GET.get('priority') or ''
    category = request.GET.get('category') or ''
    q = request.GET.get('q') or ''
    if status:
        qs = qs.filter(status=status)
    if priority:
        qs = qs.filter(priority=priority)
    if category:
        qs = qs.filter(category_id=category)
    if q:
        qs = qs.filter(title__icontains=q)
    return render(request, 'tickets/all-tickets.html', {
        'tickets': qs,
        'categories': Category.objects.all(),
        'users': User.objects.all(),
        'status_value': status,
        'priority_value': priority,
        'category_value': category,
        'q_value': q,
        'status_choices': Ticket.STATUS,
        'priority_choices': Ticket.PRIORITY,
    })

@login_required
def ticket_create(request):
    form_class = TicketForm if request.user.is_staff else UserTicketForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.created_by = request.user
            t.save()
            return redirect('ticket_detail', id=t.id)
    else:
        form = form_class()
    return render(request, 'tickets/ticket-form.html', {'form': form})

@login_required
def ticket_detail(request, id):
    t = get_object_or_404(Ticket, pk=id)
    comment_form = CommentForm()
    attachment_form = AttachmentForm()
    return render(request, 'tickets/ticket-details.html', {'ticket': t, 'comment_form': comment_form, 'attachment_form': attachment_form})

@login_required
def ticket_update(request, id):
    t = get_object_or_404(Ticket, pk=id)
    if not (request.user.is_staff or request.user == t.created_by):
        return redirect('ticket_detail', id=t.id)
    form_class = TicketForm if request.user.is_staff else UserTicketForm
    if request.method == 'POST':
        form = form_class(request.POST, instance=t)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', id=t.id)
    else:
        form = form_class(instance=t)
    return render(request, 'tickets/ticket-form.html', {'form': form})

@login_required
def ticket_delete(request, id):
    t = get_object_or_404(Ticket, pk=id)
    if not request.user.is_superuser:
        return redirect('ticket_detail', id=t.id)
    if request.method == 'POST':
        t.delete()
        return redirect('ticket_list')
    return render(request, 'tickets/ticket-delete.html', {'ticket': t})

@login_required
def comment_create(request, id):
    t = get_object_or_404(Ticket, pk=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.ticket = t
            c.author = request.user
            c.save()
    return redirect('ticket_detail', id=t.id)

@login_required
def attachment_upload(request, id):
    t = get_object_or_404(Ticket, pk=id)
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            a = form.save(commit=False)
            a.ticket = t
            a.uploaded_by = request.user
            a.save()
    return redirect('ticket_detail', id=t.id)

@login_required
def ticket_assign(request, id):
    if request.method != 'POST':
        return redirect('ticket_list')
    if not request.user.is_staff:
        return redirect('ticket_list')
    t = get_object_or_404(Ticket, pk=id)
    user_id = request.POST.get('user_id') or ''
    if user_id:
        try:
            t.assigned_to = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            t.assigned_to = None
    else:
        t.assigned_to = None
    t.save()
    return redirect('ticket_list')
