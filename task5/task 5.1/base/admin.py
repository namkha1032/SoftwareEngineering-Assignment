from django.contrib import admin

# Register your models here.

from .models import Area, User, Janitor, MCP, Collector, Transportation, Worker, Trolley_Janitor, MCP_Collector, MCP_Janitor, Vehicle_Collector, Trolley, Vehicle, ChatMessage, Area_Janitor


admin.site.register(User)
admin.site.register(Worker)
admin.site.register(MCP)
admin.site.register(Janitor)
admin.site.register(Collector)
admin.site.register(Trolley_Janitor)
admin.site.register(MCP_Collector)
admin.site.register(MCP_Janitor)
admin.site.register(Vehicle_Collector)
admin.site.register(Trolley)
admin.site.register(Vehicle)
admin.site.register(ChatMessage)
admin.site.register(Area_Janitor)
admin.site.register(Area)
