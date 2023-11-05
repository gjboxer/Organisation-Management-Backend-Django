# admin.py
from django.contrib import admin
from .models import Organization, Invitation, Task  # Import the models you want to register

# Register the models
admin.site.register(Organization)
admin.site.register(Invitation)
admin.site.register(Task)
