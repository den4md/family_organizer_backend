from django.db import models

from api.models_dir import base_task


class Subtask(base_task.BaseTask):
    task = models.ForeignKey(to='Task', on_delete=models.CASCADE, related_name='subtask_list')
