from django.contrib import admin

from api.models_dir import budget_category, budget_item, chat, chat_message, chat_user_settings, event, file, group, map_point, subtask, task, user, user_map_point

admin.site.register(budget_category.BudgetCategory)
admin.site.register(budget_item.BudgetItem)
admin.site.register(chat.Chat)
admin.site.register(chat_message.ChatMessage)
admin.site.register(chat_user_settings.ChatUserSettings)
admin.site.register(event.Event)
admin.site.register(file.File)
admin.site.register(group.Group)
admin.site.register(map_point.MapPoint)
admin.site.register(subtask.Subtask)
admin.site.register(task.Task)
admin.site.register(user.User)
admin.site.register(user_map_point.UserMapPoint)
