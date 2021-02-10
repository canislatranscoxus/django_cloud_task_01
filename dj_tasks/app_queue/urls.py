from django.urls    import path
from app_queue      import views

app_name = 'app_queue'
urlpatterns = [
    path( ''               , views.home                     , name= 'home'           ),
    path( 'create_task/'   , views.create_task              , name= 'create_task'    ),
    path( 'task_sent_ok/'  , views.task_sent_ok             , name= 'task_sent_ok'   ),
    path( 'handler_animal/', views.Handler_animal.as_view() , name= 'handler_animal' ),
    path( 'get_queue_list/', views.get_queue_list           , name= 'get_queue_list' ),
]