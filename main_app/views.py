from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm

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
def ticket_list(request):
    if request.user.is_superuser:
        qs = Ticket.objects.select_related('created_by','assigned_to')
    elif request.user.is_staff:
        qs = Ticket.objects.select_related('created_by','assigned_to').filter(assigned_to=request.user)
    else:
        qs = Ticket.objects.select_related('created_by','assigned_to').filter(created_by=request.user)
    return render(request, 'tickets/all-tickets.html', {'tickets': qs})

@login_required
def ticket_detail(request, id):
    t = get_object_or_404(Ticket.objects.select_related('created_by','assigned_to'), pk=id)
    if request.user.is_superuser or request.user == t.created_by or request.user == t.assigned_to or request.user.is_staff:
        return render(request, 'tickets/ticket-details.html', {'ticket': t})
    return redirect('ticket_list')

@login_required
def ticket_create(request):
    is_admin = request.user.is_superuser
    is_agent = request.user.is_staff and not request.user.is_superuser
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if not is_admin:
            if 'assigned_to' in form.fields:
                del form.fields['assigned_to']
        if not is_admin and not is_agent:
            if 'status' in form.fields:
                del form.fields['status']
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            if not is_admin:
                obj.assigned_to = None
            if not is_admin and not is_agent:
                obj.status = 'open'
            obj.save()
            return redirect('ticket_detail', id=obj.id)
    else:
        form = TicketForm()
        if not is_admin:
            if 'assigned_to' in form.fields:
                del form.fields['assigned_to']
        if not is_admin and not is_agent:
            if 'status' in form.fields:
                del form.fields['status']
    return render(request, 'tickets/ticket-form.html', {'form': form})

@login_required
def ticket_update(request, id):
    t = get_object_or_404(Ticket, pk=id)
    can_admin = request.user.is_superuser
    can_agent = request.user.is_staff and t.assigned_to_id == request.user.id
    if not (can_admin or can_agent):
        return redirect('ticket_detail', id=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=t)
        if not can_admin:
            if 'assigned_to' in form.fields:
                del form.fields['assigned_to']
        if form.is_valid():
            obj = form.save(commit=False)
            if not can_admin:
                obj.assigned_to_id = t.assigned_to_id
            obj.save()
            return redirect('ticket_detail', id=id)
    else:
        form = TicketForm(instance=t)
        if not can_admin:
            if 'assigned_to' in form.fields:
                del form.fields['assigned_to']
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
