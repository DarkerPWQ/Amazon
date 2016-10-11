#-*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from celery import Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website1.settings")
from django.conf import settings
app = Celery("website1")

app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))  #dumps its own request information