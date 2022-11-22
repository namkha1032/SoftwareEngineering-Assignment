from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, unique = True)
    email = models.EmailField(null =True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
    
class Worker(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)
    

class Transportation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    details =  models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)
    
class Area(models.Model):
    id= models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, default = "0")
    
    def __str__(self):
        return self.name   
    
class MCP(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, default = "0")
    capacity = models.IntegerField(default=0) 
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Trolley(Transportation):
    
    def __str__(self):
        return "Trolley " + str(self.name)
    
class Vehicle(Transportation):
    weight = models.TextField(default="Unknown") 
    capacity = models.TextField(default="Unknown") 
    fuel_cons = models.TextField(default="Unknown") 
    def __str__(self):
        return "Vehicle " + str(self.name)
    
class Janitor(Worker):
    
    mcps = models.ManyToManyField(MCP, through='MCP_Janitor')
    trolleys = models.ManyToManyField(Trolley, through='Trolley_Janitor')
    areas = models.ManyToManyField(Area, through='Area_Janitor')
    
    def __str__(self):
        return "Janitor " + str(self.name)


class Collector(Worker):
    
    mcps = models.ManyToManyField(MCP, through='MCP_Collector')
    vehicles = models.ManyToManyField(Vehicle, through='Vehicle_Collector')
    
    def __str__(self):
        return "Collector " + str(self.name)

class MCP_Janitor(models.Model):
    janitor = models.ForeignKey(Janitor, on_delete=models.CASCADE)
    mcp = models.ForeignKey(MCP, on_delete=models.CASCADE)
    work_date = models.DateField()
    
    def __str__(self):
        return "{}_{}_{}".format(self.janitor.__str__(), self.mcp.__str__(), self.work_date)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['janitor', 'work_date'], name='mcp_janitor_date'
            )
        ]
        ordering = ['work_date']
    
class Area_Janitor(models.Model):
    janitor = models.ForeignKey(Janitor, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    work_date = models.DateField()
    
    def __str__(self):
        return "{}_{}_{}".format(self.janitor.__str__(), self.area.__str__(), self.work_date)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['janitor', 'work_date'], name='area_janitor_date'
            )
        ]
        ordering = ['work_date']
        
    
class MCP_Collector(models.Model):
    collector = models.ForeignKey(Collector, on_delete=models.CASCADE)
    mcp = models.ForeignKey(MCP, on_delete=models.CASCADE)
    work_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{}_{}_{}".format(self.collector.__str__(), self.mcp.__str__(), self.work_date)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['collector', 'mcp', 'work_date'], name='mcp_collector_date'
            )
        ]
    
class Vehicle_Collector(models.Model):
    collector = models.ForeignKey(Collector, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    work_date = models.DateField()
    
    def __str__(self):
        return "{}_{}_{}".format(self.collector.__str__(), self.vehicle.__str__(), self.work_date)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['collector', 'work_date'], name='vehicle_collector_date'
            )
        ]
    
class Trolley_Janitor(models.Model):
    janitor = models.ForeignKey(Janitor, on_delete=models.CASCADE)
    trolley = models.ForeignKey(Trolley, on_delete=models.CASCADE)
    work_date = models.DateField()
    
    def __str__(self):
        return "{}_{}_{}".format(self.janitor.__str__(), self.trolley.__str__(), self.work_date)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['janitor', 'work_date'], name='trolley_janitor_date'
            )
        ]
    
class Calendar(models.Model):
    date = models.DateField(null=True)
    
class ChatMessage(models.Model):
    body = models.TextField(null=False, blank=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Worker, on_delete=models.CASCADE)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', 'created']
        
    def __str__(self):
        return self.body[0:50]


