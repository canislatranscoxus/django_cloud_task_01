from django.shortcuts import render, redirect
from . import forms
from app_queue.Qmessenger import Qmessenger

# Create your views here.

def home( request ):
    return render( request, 'gui/home.html' )    

def create_task( request ):
    #

    payload  = {
                'animal' : 'dog',
                'name'   : 'Spike',
                'age'    : 1
            }

    form    = forms.AnimalForm( initial= payload )
    dic = {}

    if request.method=='POST':
        form = forms.AnimalForm( request.POST )
        if form.is_valid():
            payload = {
                        'animal' : form.cleaned_data[ 'animal'  ],
                        'name'   : form.cleaned_data[ 'name'    ],
                        'age'    : form.cleaned_data[ 'age'     ]
                      }            

            qmessenger = Qmessenger()
            qmessenger.add( payload )
            
            return redirect( 'app_queue:task_sent_ok' )
            #return render(request, '/gui/task_sent_ok.html' )

    dic[ 'form' ] = form
    return render( request, 'gui/create_task.html', dic )

def task_sent_ok( request ):
    return render(request, 'gui/task_sent_ok.html')


def handler_animals():
    pass

def get_queue_list():
    # we get the task that are in the queue
    pass    

def get_my_list():
    # we show the tasks we have created and added to the queue
    pass    
