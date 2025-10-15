from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm, UserTicketForm, CommentForm, AttachmentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class Home(LoginView):
    template_name = 'registration/login.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ticket_list')
        else:
            error_message = 'Invalid sign up'
    form = UserCreationForm()
    return render(request, 'signup.html', {'form': form, 'error_message': error_message})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        my_open = Ticket.objects.filter(status__in=['open','in_progress']).count()
        assigned_to_me = Ticket.objects.filter(assigned_to=request.user).count()
        resolved = Ticket.objects.filter(status__in=['resolved','closed']).count()
    elif request.user.is_staff:
        my_open = Ticket.objects.filter(assigned_to=request.user, status__in=['open','in_progress']).count()
        assigned_to_me = Ticket.objects.filter(assigned_to=request.user).count()
        resolved = Ticket.objects.filter(assigned_to=request.user, status__in=['resolved','closed']).count()
    else:
        my_open = Ticket.objects.filter(created_by=request.user, status__in=['open','in_progress']).count()
        assigned_to_me = 0
        resolved = Ticket.objects.filter(created_by=request.user, status__in=['resolved','closed']).count()
    return render(request, 'dashboard.html', {'my_open': my_open, 'assigned_to_me': assigned_to_me, 'resolved': resolved})

@login_required
def ticket_list(request):
    if request.user.is_superuser:
        qs = Ticket.objects.select_related('created_by','assigned_to','category')
    elif request.user.is_staff:
        qs = Ticket.objects.select_related('created_by','assigned_to','category').filter(assigned_to=request.user)
    else:
        qs = Ticket.objects.select_related('created_by','assigned_to','category').filter(created_by=request.user)
    return render(request, 'tickets/all-tickets.html', {'tickets': qs})

@login_required
def ticket_detail(request, id):
    t = get_object_or_404(Ticket.objects.select_related('created_by','assigned_to','category'), pk=id)
    if request.user.is_superuser or request.user.is_staff or request.user == t.created_by or request.user == t.assigned_to:
        return render(request, 'tickets/ticket-details.html', {
            'ticket': t,
            'comment_form': CommentForm(),
            'attachment_form': AttachmentForm(),
        })
    return redirect('ticket_list')

@login_required
def ticket_create(request):
    is_admin = request.user.is_superuser
    is_agent = request.user.is_staff and not request.user.is_superuser
    form_class = TicketForm if (is_admin or is_agent) else UserTicketForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            if not is_admin:
                obj.assigned_to = None
            if not (is_admin or is_agent):
                obj.status = 'open'
            obj.save()
            return redirect('ticket_detail', id=obj.id)
    else:
        form = form_class()
    return render(request, 'tickets/ticket-form.html', {'form': form})

@login_required
def ticket_update(request, id):
    t = get_object_or_404(Ticket, pk=id)
    can_admin = request.user.is_superuser
    can_agent = request.user.is_staff and t.assigned_to_id == request.user.id
    if not (can_admin or can_agent):
        return redirect('ticket_detail', id=id)
    form = TicketForm(request.POST or None, instance=t)
    if not can_admin:
        if 'assigned_to' in form.fields:
            del form.fields['assigned_to']
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        if not can_admin:
            obj.assigned_to_id = t.assigned_to_id
        obj.save()
        return redirect('ticket_detail', id=id)
    return render(request, 'tickets/ticket-form.html', {'form': form})

@login_required
def ticket_delete(request, id):
    t = get_object_or_404(Ticket, pk=id)
    if not request.user.is_superuser:
        return redirect('ticket_detail', id=id)
    if request.method == 'POST':
        t.delete()
        return redirect('ticket_list')
    return render(request, 'tickets/ticket-delete.html', {'ticket': t})

@login_required
def comment_create(request, id):
    t = get_object_or_404(Ticket, pk=id)
    if not (request.user.is_superuser or request.user.is_staff or request.user == t.created_by or request.user == t.assigned_to):
        return redirect('ticket_list')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.ticket = t
            c.author = request.user
            c.save()
    return redirect('ticket_detail', id=id)

@login_required
def attachment_upload(request, id):
    t = get_object_or_404(Ticket, pk=id)
    if not (request.user.is_superuser or request.user.is_staff or request.user == t.created_by or request.user == t.assigned_to):
        return redirect('ticket_list')
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            a = form.save(commit=False)
            a.ticket = t
            a.uploaded_by = request.user
            a.save()
    return redirect('ticket_detail', id=id)



def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ticket_list')
        else:
            error_message = 'Invalid sign up'
    form = UserCreationForm()
    return render(request, 'signup.html', {'form': form, 'error_message': error_message})
