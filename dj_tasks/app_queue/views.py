import json
from pprint                         import pprint
from googleapiclient                import discovery
from oauth2client.client            import GoogleCredentials

from django.shortcuts import render, redirect
from rest_framework.views           import APIView
from rest_framework.response        import Response
from rest_framework.authentication  import BasicAuthentication
from rest_framework.permissions     import AllowAny, IsAuthenticated

from . import forms
from app_queue.Qmessenger import Qmessenger


# Create your views here.

def home( request ):
    return render( request, 'gui/home.html' )    

def create_task( request ):
    payload  = {
                'animal' : 'dog',
                'name'   : 'Spike',
                'age'    : 1
            }

    form    = forms.AnimalForm( initial= payload )
    dic     = {}

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


class Handler_animal( APIView ):
    authentication_classes  = ( BasicAuthentication, )
    permission_classes      = ( AllowAny,)

    def post(self, request, *args, **kwargs):
        print( 'app_queue.views.Handler_animal.post() ... begin' )
        print( 'payload: ' )
        payload = request.data
        s = json.dumps( payload, indent = 4 )
        print( s )
        print( 'app_queue.views.Handler_animal.post() ... end' )
        return Response( data = payload )




def get_queue_list( request ):
    # we get the task that are in the queue
    qmessenger  = Qmessenger()
    credentials = GoogleCredentials.get_application_default()
    service     = discovery.build('cloudtasks', 'v2beta3', credentials=credentials)

    request = service.projects().locations().queues().tasks().list( parent = qmessenger.parent )
    task_list = []
    while True:
        response = request.execute()

        for task in response.get('tasks', []):
            # TODO: Change code below to process each `task` resource:
            pprint(task)
            task_list.append( task[ 'name' ] )

        request = service.projects().locations().queues().tasks().list_next(previous_request=request, previous_response=response)
        if request is None:
            break
    
    return render( request, 'gui/get_queue_list.html', { 'task_list': task_list } )

def get_my_list( request ):
    # we show the tasks we have created and added to the queue
    pass    
