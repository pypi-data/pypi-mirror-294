import tempfile
from uuid import uuid4
from datetime import datetime

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.http import HttpResponse
from django.template import Template, Context, loader

class RenderAsMessage(object):
    def get_template(self, template:str="singular_result"):
        
        singular_result = """
        <h2>{{ title }}</h2>
        <p>{{ description|safe }}</p>
        """
        progress = """
        {% load static %}
        <div class='progress-wrapper'>
          <div id='progress-bar' class='progress-bar' style="background-color: #68a9ef; width: 0%;">&nbsp;</div>
        </div>
        <div id="progress-bar-message">Waiting for progress to start...</div>
        <script src="{% static 'celery_progress/celery_progress.js' %}"></script>
        <script>
        document.addEventListener("DOMContentLoaded", function () {
          var progressUrl = "{% url 'admin:get_progress' task_id %}";
          CeleryProgressBar.initProgressBar(progressUrl);
        });
        </script>
        """
        templates = {
            "singular_result": singular_result,
            "progress": progress,
        }
        
        return templates[template]

    def render_as_snippet(self, context, template="singular_result"):
        template_string = self.get_template(template=template)
        template = Template(template_string)
        context = Context(context)
        return template.render(context)
    
    def render_as_message(self, request, context, template="singular_result"):
        
        template_string = self.get_template(template=template)
        template = Template(template_string)
        context = Context(context)
        self.message_user(request, template.render(context))


