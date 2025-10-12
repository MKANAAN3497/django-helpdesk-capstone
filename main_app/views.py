from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Category
from .forms import TicketForm, CategoryForm

def homepage(request):
    return render(request, 'homepage.html')

def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/all-tickets.html', {'tickets': tickets})

def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    return render(request, 'tickets/ticket-details.html', {'ticket': ticket})

def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket-form.html', {'form': form})

def ticket_update(request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'tickets/ticket-form.html', {'form': form})

def ticket_delete(request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('ticket_list')
    return render(request, 'tickets/ticket-delete.html', {'ticket': ticket})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/all-categories.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'categories/category-form.html', {'form': form})
