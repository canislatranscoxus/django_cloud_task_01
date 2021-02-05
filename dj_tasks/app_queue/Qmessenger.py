'''
This class is a Queue Messenger that send a message 
from this app to the queue, 
that message says add a new task to the queue.
'''

from __future__             import print_function
from django.conf            import settings

#from google.cloud import tasks_v2
from google.cloud           import tasks_v2beta3
from google.cloud           import tasks

from googleapiclient        import discovery
from oauth2client.client    import GoogleCredentials


import datetime
import json


class Qmessenger:

    client  = None
    parent  = None
    service = None

    def add_gae( self, payload ):
        '''params is a dictionary '''
        relative_uri = '/app_queue/handler_animals'
        
        if 'url' in payload:
            relative_uri = payload[ 'url' ]

        print( 'Qmessenger.add_gae()....' )

        #task_name = '{order_id}_{doc_type}'.format( **params )

        # Construct the request body.

        task = {
            #'view'        : tasks.Task.View.FULL ,
            #'response_view' : tasks.Task.View.FULL ,

            'http_request': {},

            'app_engine_http_request': {  
                #'http_method'  : 'POST',
                #'http_method'  : tasks_v2.HttpMethod.POST,
                'http_method'  : tasks_v2beta3.HttpMethod.POST,
                'relative_uri' : relative_uri,
                'body'         : ''
            }
        }

        if payload is not None:
            if isinstance(payload, dict):
                # Convert dict to JSON string
                spayload = json.dumps(payload)
                
                # specify http content-type to application/json
                task[ 'http_request' ][ 'headers' ] = { 'Content-type': 'application/json' }

            # The API expects a payload of type bytes.
            converted_payload = spayload.encode()

            # Add the payload to the request.
            #task['app_engine_http_request'][ 'body' ] = converted_payload
            task['app_engine_http_request'][ 'body' ] = spayload


        create_task_request_body = {
            'task'          : task,
            'responseView'  : tasks.Task.View.FULL  
            #self.service.projects().locations().queues().tasks().View().FULL
        }

        request  = self.service.projects().locations().queues().tasks().create(
                    parent = self.parent, 
                    body=create_task_request_body )
        response = request.execute()


        # Use the client to build and send the task.
        response = self.client.create_task( parent = self.parent, task=task )

        print('Created task {}'.format( response.name ))
        




    def add_http( self, payload ):
        '''params is a dictionary '''
        print( 'Mail_queue_gcp.add_http()....' )

        # Construct the request body.
        task = {
            'http_request': {  # Specify the type of request.
                #'http_method' : tasks_v2.HttpMethod.POST,
                'http_method' : tasks_v2beta3.HttpMethod.POST,
                'url'         : 'https://basmatiyes.ue.r.appspot.com/app_queue/handler_animals/' ,
                'headers'     : '',
                'body'        : ''
            }
        }

        if payload is not None:
            if isinstance(payload, dict):
                # Convert dict to JSON string
                payload = json.dumps(payload)
                
                # specify http content-type to application/json
                task[ 'http_request' ][ 'headers' ] = { 'Content-type': 'application/json' }


            # The API expects a payload of type bytes.
            converted_payload = payload.encode()

            # Add the payload to the request.
            task[ 'http_request' ][ 'body' ] = converted_payload

        # Use the client to build and send the task.
        response = self.client.create_task(request={"parent": self.parent, "task": task})
        print('Created task {}'.format( response.name ))
        return response

    def add( self, payload):
        try:
            self.add_gae ( payload )
            #self.add_http( params )
        except Exception as e:
            print( 'Qmessenger.add(), error: {}'.format( e ) )
            raise

    def __init__(self ):

        credentials = GoogleCredentials.get_application_default()
        self.service = discovery.build('cloudtasks', 'v2beta3', credentials=credentials)

        #service     = discovery.build('cloudtasks', 'v2beta3', credentials=credentials)
        #service.projects().locations().queues().tasks().create(  )

        # Create a client.
        #client = tasks_v2.CloudTasksClient()
        client = tasks_v2beta3.CloudTasksClient(  )

        # TODO(developer): Uncomment these lines and replace with your values.
        project  = settings.PROJECT
        location = settings.LOCATION
        queue    = settings.QUEUE_NAME

        # Construct the fully qualified queue name.
        #parent = client.queue_path(project, location, queue)
        self.parent = client.queue_path(project, location, queue)

        self.client = client
        
        print( 'Qmessenger._init_ created  😊k.' )