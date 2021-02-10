
# Readme
## django_cloud_task_01

This is a small example using google cloud task and a django python application running in 
google App Engine. The main idea is to show how to create a task in a queue that lives in google cloud tasks, using our django app. 

The task include a payload that is a json, with three fields:
* animal,   is string
* name,     is string
* age,      is an integer

Later cloud tasks is going to call a handler in our django app
called Handler_animal. This class will read the payload and make a simple process
print to console and create two objects in a bucket in google storage.

# Steps to run our example

First create a project in GCP (Google Cloud Platform),
create a queue in google Cloud Tasks
create a bucket in Storage.

Then, open Google Cloud Shell and follow the next steps.

## install some libraries in Google Cloud Shell

```sh
sudo apt-get install python3-venv
python3 -m venv env
source env/bin/activate

pip3 install --upgrade pip
python3 -m pip install --upgrade setuptools
pip3 install --no-cache-dir  --force-reinstall -Iv grpcio==1.35.0 

git clone https://github.com/canislatranscoxus/django_cloud_task_01.git
cd django_cloud_task_01/dj_tasks/
pip install -r requirements.txt
```

## Update Environment variables in app.yaml
In app.yaml use your data of your project id, location, queue and bucket name to update the next variables

```python
env_variables:
#  add the environment variables HERE
  PROJECT: "#TODO my-project-HERE"
  LOCATION: "#TODO my-location-HERE"
  QUEUE_NAME: "#TODO my-queue-name-HERE"
  BUCKET_NAME: "#TODO my-bucket-name-HERE"
```

## Deploy Code to App Engine

run the following commands

```sh
gcloud app deploy
```
A window will emerge and ask your authorization, Authorize and continue. 


```sh
gcloud app browse
```
next click the link that will appear on the console


### how to use the web app

click the link for ```create task ```
give some values in the form
create the task
go to monitor the print messages
also, check your bucket, you must have 2 new objects. 

The object ```handler_animal.txt```, is confirming that the handler was loaded.
```handler_animal_data.txt``` must have a json of your task payload, that is the data you entered in the web form. 


## monitor our app running in app engine

To see all the print messages, run the next command 

```sh
gcloud app logs tail -s default 
```

## references
create task
* https://cloud.google.com/tasks/docs/creating-appengine-tasks

projects.locations.queues.tasks.list
* https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/list

GCP cloud tasks with Django
* https://rimvydas.com/publications/gcp_django_tasks/

python-docs-samples
* https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/flexible/tasks/create_app_engine_queue_task.py

Averikitsch / python-docs-samples 
* https://github.com/averikitsch/python-docs-samples/tree/flask-task/tasks