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
