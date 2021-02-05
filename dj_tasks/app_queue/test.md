# Test

here we have some test cases.

## how to test locally the handler

curl -i -X POST http://127.0.0.1:8000/handler_animal/   \
-H "Content-Type: application/json"                     \
-d '{ "animal": "cat", "name":"Little Paws", "age": 2 }'        

## how to get the list of task from queue in Cloud Tasks.
gcloud tasks list --queue=my-queue


## references
https://cloud.google.com/sdk/gcloud/reference/tasks/list


## data for testing

parent : 'projects/basmatiyes/locations/us-east1/queues/qshop'

create_task_request_body:
{
    'responseView': <View.FULL: 2>, 
    'task': 
    
    {   'app_engine_http_request': {
            'body'          : b'{"animal": "dog", "name": "Spike", "age": 1.0}',          
            'http_method'   : <HttpMethod.POST: 1>, 
            'relative_uri'  : '/app_queue/handler_animals'}, 
        
        'http_request'  : {'headers': {'Content-type': 'application/json'} }, 
        'view'          : <View.FULL: 2>
    }

    'http_request': {...}, 'view': <View.FULL: 2>}
}