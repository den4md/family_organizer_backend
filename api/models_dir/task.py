from django.db import models

from api.models_dir import base_task


class Task(base_task.BaseTask):
    is_task = models.BooleanField(default=False)  # when False this is Note
    group = models.ForeignKey(to='Group', on_delete=models.CASCADE, related_name='task_list')
