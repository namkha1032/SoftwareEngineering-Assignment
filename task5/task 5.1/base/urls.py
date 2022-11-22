from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('collector/<str:pk>/<str:date_time>', views.collector_page, name="collector"),
    path('janitor/<str:pk>/<str:date_time>', views.janitor_page, name="janitor"),
    path('janitor_date/<str:pk>/', views.janitor_date, name="janitor_date"),
    path('collector_date/<str:pk>/', views.collector_date, name="collector_date"),
    path('update_janitor_mcp/<str:pk>/<str:date_time>', views.update_janitor_mcp, name="update_janitor_mcp"),
    path('update_janitor_trolley/<str:pk>/<str:date_time>', views.update_janitor_trolley, name="update_janitor_trolley"),
    path('update_janitor_area/<str:pk>/<str:date_time>', views.update_janitor_area, name="update_janitor_area"),
    path('add_collector_mcp/<str:pk>/<str:date_time>', views.add_collector_mcp, name="add_collector_mcp"),
    path('delete_collector_mcp/<str:pk>/<str:date_time>', views.delete_collector_mcp, name="delete_collector_mcp"),
    path('update_collector_vehicle/<str:pk>/<str:date_time>', views.update_collector_vehicle, name="update_collector_vehicle"),
    path('', views.home_page, name="home_page"),
    path('chat/<str:pk>', views.chat, name="chat"),
    path('update_msg/<str:pk>', views.update_msg, name="update_msg"),
    
]
