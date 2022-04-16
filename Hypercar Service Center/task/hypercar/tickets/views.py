from collections import deque
from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

ticket_no = 0
ticket_process = 0
change_oil_deque = deque()
inflate_tires_deque = deque()
diagnostic_deque = deque()
line_of_cars = {'change_oil': change_oil_deque, 'inflate_tires': inflate_tires_deque,
                'diagnostic': diagnostic_deque}


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')


class GetTicket(View):
    def get(self, request, link, *args, **kwargs):
        global ticket_no, change_oil_deque, inflate_tires_deque, diagnostic_deque
        ticket_no += 1
        l_change = len(change_oil_deque)
        l_inflate = len(inflate_tires_deque)
        l_diagnostic = len(diagnostic_deque)
        # ticket_no = l_change + l_inflate + l_diagnostic + 1
        if link == 'change_oil':
            change_oil_deque.append(ticket_no)
            time = l_change * 2
        elif link == 'inflate_tires':
            inflate_tires_deque.append(ticket_no)
            time = l_change * 2 + l_inflate * 5
        elif link == 'diagnostic':
            diagnostic_deque.append(ticket_no)
            time = l_change * 2 + l_inflate * 5 + l_diagnostic * 30
        else:
            print('Wrong service')
        return render(request, 'tickets/get_ticket.html', context={'ticket_no': ticket_no, 'time': time})


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        global ticket_no, change_oil_deque, inflate_tires_deque, diagnostic_deque
        l_change = len(change_oil_deque)
        l_inflate = len(inflate_tires_deque)
        l_diagnostic = len(diagnostic_deque)
        return render(request, 'tickets/processing.html', context={'l_change': l_change, 'l_inflate': l_inflate,
                                                                   'l_diagnostic': l_diagnostic})

    def post(self, request, *args, **kwargs):

        global ticket_process
        # ...things to do, to create a number of the ticket, which is under processing...
        if len(change_oil_deque) > 0:
            ticket_process = change_oil_deque.popleft()
        elif len(inflate_tires_deque) > 0:
            ticket_process = inflate_tires_deque.popleft()
        elif len(diagnostic_deque) > 0:
            ticket_process = diagnostic_deque.popleft()
        else:
            ticket_process = 0

        return redirect('/next/')


class NextView(View):
    def get(self, request, *args, **kwargs):
        global ticket_process
        return render(request, 'tickets/next.html', context={'ticket_process': ticket_process})
