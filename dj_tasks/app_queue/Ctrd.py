'''
Description: This class represent the Cloud Tasks Request Defense.
             Here we can see if the request is from Google Cloud Task,
             and if the Queue belongs to our project.
'''

class Ctrd:

    @staticmethod
    def is_from_cloud_tasks( request, queue_name ):
        try:
            gae_headers = [
                'HTTP_USER_AGENT', 
                'CONTENT_TYPE', 
                'HTTP_X_APPENGINE_QUEUENAME', 
                'HTTP_X_APPENGINE_TASKNAME', 
                'HTTP_X_APPENGINE_TASKRETRYCOUNT', 
                'HTTP_X_APPENGINE_TASKEXECUTIONCOUNT', 
                'HTTP_X_APPENGINE_TASKETA', 
                'HTTP_X_APPENGINE_COUNTRY', 
                'HTTP_X_APPENGINE_TIMEOUT_MS', 
                'HTTP_X_APPENGINE_HTTPS', 
                'HTTP_X_APPENGINE_USER_IP', 
                'HTTP_X_GOOGLE_INTERNAL_SKIPADMINCHECK', 
                'HTTP_X_APPENGINE_REQUEST_LOG_ID', 
                'HTTP_X_APPENGINE_DEFAULT_VERSION_HOSTNAME', 
            ]
            # verify request has all the headers
            for header in gae_headers:
                if header not in request.META:
                    return False 

            if request.META[ 'HTTP_USER_AGENT' ] == 'AppEngine-Google; (+http://code.google.com/appengine)' \
                and 'HTTP_X_APPENGINE_QUEUENAME' == queue_name:
                return True

        except Exception as e:
            print( 'Ctrd.is_from_cloud_tasks(), error: {}'.format( e ) )
        
        return False