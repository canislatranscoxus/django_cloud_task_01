# django_cloud_task_01

This is a small example using django python library and cloud task.
The main idea is to show how to create a task in one queue that lives in cloud tasks,
using our django app. 

The task include a payload that is a json, with three fields:
* animal
* name
* age

Later cloud tasks is going to call a handler in our django app
called Handler_animal. This class will read the payload and make a simple process
print to console.


## references
create task
* https://cloud.google.com/tasks/docs/creating-appengine-tasks

projects.locations.queues.tasks.list
* https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/list

GCP cloud tasks with Django
* https://rimvydas.com/publications/gcp_django_tasks/

Averikitsch / python-docs-samples 
* https://github.com/averikitsch/python-docs-samples/tree/flask-task/tasks