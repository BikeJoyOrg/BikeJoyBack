from django.contrib import admin
from .models import Achievement, AchievementProgress
from .models import Level

admin.site.register(Achievement)
admin.site.register(Level)
admin.site.register(AchievementProgress)
