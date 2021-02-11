import json
from pprint                         import pprint
from googleapiclient                import discovery
from oauth2client.client            import GoogleCredentials

from django.shortcuts               import render, redirect
from django.conf                    import settings

from rest_framework.parsers         import JSONParser
from rest_framework.views           import APIView
from rest_framework.response        import Response
from rest_framework.authentication  import BasicAuthentication
from rest_framework.permissions     import AllowAny

from . import forms
from app_queue.Qmessenger import Qmessenger
from app_queue.GCS        import GCS



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

    parser_classes          = [JSONParser]
    bucket_name             = settings.BUCKET_NAME

    def post(self, request, *args, **kwargs):
        payload = 'handler_animal begin'
        try:
            
            print( 'app_queue.views.Handler_animal.post() ... begin' )
            GCS.upload_blob_from_string( self.bucket_name, 'Handler_animal loaded', 'handler_animal.txt' )

            print( 'request attributes: \n {}'.format( dir( request ) ) )

            print( 'searching gae_headers ...' )
            gae_headers = [ 'X-AppEngine-QueueName'
            , 'X-AppEngine-TaskName'
            , 'X-AppEngine-TaskRetryCount' ]

            for i in gae_headers:
                try:
                    if i in request:
                        print( 'request has header: {}'.format(i) )
                        print( request[ i ] )
                except Exception as e:
                    print( 'error searching {}'.format( i ) )



            print( 'META' )
            s = json.dumps( request.META, indent= 4 )
            print( s )

            print( 'getting body' )
            b = request.body
            print( 'type(b) is: {}'.format( type(b) ) )
            print( 'body: {}'.format( b ) )

            print( 'getting payload ' )
            payload = request.body

            print( 'type ( body ): {}'.format( type( payload ) ) )

            if isinstance(payload, dict):
                print( 'dumping dict payload to string' )
                s = json.dumps( payload, indent = 4 )
                print( s )
            else:
                print( 'decoding payload from bytes to json' )
                payload = request.body.decode('utf8').replace("'", '"')
                print( 'type( payload ): {}'.format( type( payload ) ) )
                j = json.loads( payload )
                print( 'animal: {}'.format( j[ 'animal' ] ) )

                txt = json.dumps( j, indent= 4 )
                print( 'json payload' )
                print( txt )
                
                print( 'decoding from bytes to string' )
                s = request.body.decode('utf8')
                print( 'type(s): {}'.format( type(s) ) )
                print( 's: {}'.format( s ) )

            GCS.upload_blob_from_string( self.bucket_name, s, 'handler_animal_data.txt' )
            print( 'app_queue.views.Handler_animal.post() ... end' )
        except Exception as e:
            print( 'Handler_animal.post(), error: {}'.format( e ) )
            
        return Response( data = payload )



def h2( request ):
    try:
        print( 'app_queue.views.h2(), ... begin' )
        if request.method == 'POST':
            print( 'request method is POST' )

        print( 'type( data ): {}'.format(  type(request.data) ) )
        print( 'data        : {}'.format(  request.data  ) )
    except Exception as e:
        print( 'app_queue.views.h2(), error: {}'.format( e ) )

    print( 'app_queue.views.h2(), ... end' )


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

