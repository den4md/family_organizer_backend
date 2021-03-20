import importlib

models_dir_list = ['budget_category', 'budget_item', 'chat', 'chat_message', 'chat_user_settings',
                   'event', 'file', 'group', 'map_point', 'subtask', 'task', 'user', 'user_map_point']

for models_dir in models_dir_list:
    importlib.import_module('api.models_dir.' + models_dir)
