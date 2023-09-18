# your_app/tasks.py

from celery import shared_task
from .celery import *
@shared_task
def hello_world():
    print("Hello, World!")
    
 

hello_world.delay()  
