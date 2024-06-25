from app import forms, views
from .forms import TicketsForm

def add_ticket_form(request):
    return {
        'ticket_form': TicketsForm()
    }
