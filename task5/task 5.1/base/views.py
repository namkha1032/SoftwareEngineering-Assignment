from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User, Janitor, Collector, Vehicle, Area_Janitor, ChatMessage
from .models import Trolley, MCP, MCP_Collector, MCP_Janitor, Vehicle_Collector, Trolley_Janitor, Area, Worker
from .forms import MyUserCreationForm, DateForm
import datetime


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home_page')

@login_required(login_url='login')
def home_page(request):
    janitors = Janitor.objects.all()
    collectors = Collector.objects.all()
    vehicles = Vehicle.objects.all()
    trolleys = Trolley.objects.all()
    mcps = MCP.objects.all()
    areas = Area.objects.all()
    date_time = datetime.date.today()
    
    vehicle_list=[]
    for item in Vehicle_Collector.objects.filter(work_date=date_time):
        vehicle_list.append(item.vehicle)
        
    troley_list=[]
    for item in Trolley_Janitor.objects.filter(work_date=date_time):
        troley_list.append(item.trolley)
    context ={'janitors': janitors, 'collectors': collectors, 'vehicles': vehicles,
              'trolleys': trolleys, 'mcps': mcps, 'areas': areas, 'date': date_time.strftime("%Y-%m-%d"),
              'vehicle_list':vehicle_list, 'troley_list':troley_list}
    
    return render(request, 'home.html', context)

@login_required(login_url='login')
def collector_page(request, pk, date_time):
    collector = Collector.objects.get(id = pk)
    date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d').date()
    mcp_list = MCP_Collector.objects.filter(collector = collector, work_date = date_time).order_by('created')
    used_mcp =[]
    for item in mcp_list:
        used_mcp.append(item.mcp)
    vehicle_date = Vehicle_Collector.objects.filter(collector = collector, work_date = date_time).first()
    used_vehicle=[]
    for item in Vehicle_Collector.objects.filter(work_date=date_time):
        used_vehicle.append(item.vehicle)
    ori = ""
    dest = ""
    if(len(used_mcp)):
        ori = used_mcp[0]
        dest = used_mcp[-1]
    waypoint = ""
    for mcp in used_mcp:
        if mcp != ori and mcp != dest:
            waypoint += (mcp.location + "|")
    waypoint = waypoint[:-1]
    context = {'collector':collector, 'used_mcp':used_mcp, 'date': str(date_time), 'vehicle_date': vehicle_date,
               'mcp_all': MCP.objects.all(), 'used_vehicle': used_vehicle, 'vehicle_all': Vehicle.objects.all(),
               'used_mcp_count': len(used_mcp), 'ori': ori, 'dest': dest, 'waypoint': waypoint}
    return render(request, 'collector.html', context)

@login_required(login_url='login')
def collector_date(request, pk):
    if request.method == "POST":
        date_time = request.POST.get('my_date_field')
        return redirect('collector', pk=pk, date_time = date_time)


@login_required(login_url='login')
def add_collector_mcp(request, pk, date_time):

    if request.method == "POST":
        date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d')
        collector = Collector.objects.get(id = pk)
        chosen_mcp = MCP.objects.get(id = request.POST.get('chosenmcp'))

        MCP_Collector.objects.create(collector=collector, work_date=date_time, mcp = chosen_mcp)
        return redirect('collector', pk = pk, date_time = date_time.strftime("%Y-%m-%d"))
    
@login_required(login_url='login')
def delete_collector_mcp(request, pk, date_time):

    if request.method == "POST":
        date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d')
        collector = Collector.objects.get(id = pk)
        chosen_mcp = MCP.objects.get(id = request.POST.get('chosenmcp'))
        MCP_Collector.objects.filter(work_date=date_time, collector = collector, mcp = chosen_mcp).delete()

        return redirect('collector', pk = pk, date_time = date_time.strftime("%Y-%m-%d")) 
    
@login_required(login_url='login')
def update_collector_vehicle(request, pk, date_time):

    if request.method == "POST":
        date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d')
        collector = Collector.objects.get(id = pk)
        chosen_vehicle = Vehicle.objects.get(id = request.POST.get('chosenvehicle'))
        
        obj, created = Vehicle_Collector.objects.update_or_create(collector=collector, work_date=date_time, 
                                                                  defaults = {'vehicle': chosen_vehicle})
        return redirect('collector', pk = pk, date_time = date_time.strftime("%Y-%m-%d"))
    
@login_required(login_url='login')
def janitor_page(request, pk, date_time):
    janitor = Janitor.objects.get(id = pk)
    date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d').date()
    mcp_list = MCP_Janitor.objects.filter(janitor = janitor, work_date = date_time)
    area_list = Area_Janitor.objects.filter(janitor = janitor, work_date = date_time)
    mcp_date = mcp_list.first()
    used_area = area_list.first()
    trolley_date = Trolley_Janitor.objects.filter(janitor = janitor, work_date = date_time).first()
    used_trolley=[]
    for item in Trolley_Janitor.objects.filter(work_date=date_time):
        used_trolley.append(item.trolley)
        
    map_choice = -1
    
    if(mcp_list.count() == 0 and area_list.count() == 0):
        map_choice = 0
    elif (mcp_list.count() != 0 and area_list.count() == 0):
        map_choice = 1
    elif (mcp_list.count() == 0 and area_list.count() != 0):
        map_choice = 2
    else:
        map_choice = 3
        
        
    context = {'janitor':janitor, 'mcp_date':mcp_date, 'date': str(date_time), 'trolley_date': trolley_date,
               'mcp_all': MCP.objects.all(), 'used_trolley': used_trolley, 'trolley_all': Trolley.objects.all(),
               'area_all': Area.objects.all(), 'used_area':used_area, 'map_choice': map_choice}
    return render(request, 'janitor.html', context)
    
@login_required(login_url='login')
def janitor_date(request, pk):
    if request.method == "POST":
        date_time = request.POST.get('my_date_field')
        return redirect('janitor', pk=pk, date_time = date_time)

@login_required(login_url='login')
def update_janitor_mcp(request, pk, date_time):

    if request.method == "POST":
        date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d')
        janitor = Janitor.objects.get(id = pk)
        chosen_mcp = MCP.objects.get(id = request.POST.get('chosenmcp'))

        obj, created = MCP_Janitor.objects.update_or_create(janitor=janitor, work_date=date_time, defaults = {'mcp': chosen_mcp})
        return redirect('janitor', pk = pk, date_time = date_time.strftime("%Y-%m-%d"))

@login_required(login_url='login')
def update_janitor_trolley(request, pk, date_time):

    if request.method == "POST":
        date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d')
        janitor = Janitor.objects.get(id = pk)
        chosen_trolley = Trolley.objects.get(id = request.POST.get('chosentrolley'))
        
        obj, created = Trolley_Janitor.objects.update_or_create(janitor=janitor, work_date=date_time, defaults = {'trolley': chosen_trolley})
        return redirect('janitor', pk = pk, date_time = date_time.strftime("%Y-%m-%d"))

@login_required(login_url='login')
def update_janitor_area(request, pk, date_time):

    if request.method == "POST":
        date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d')
        janitor = Janitor.objects.get(id = pk)
        chosen_area = Area.objects.get(id = request.POST.get('chosenarea'))

        obj, created = Area_Janitor.objects.update_or_create(janitor=janitor, work_date=date_time, defaults = {'area': chosen_area})
        return redirect('janitor', pk = pk, date_time = date_time.strftime("%Y-%m-%d"))
    
@login_required(login_url='login')
def chat(request,pk):
    current_user = request.user
    worker = Worker.objects.get(id=pk)
    msgs = ChatMessage.objects.filter(sender=current_user, receiver = worker).order_by('created')
    
    
    context={'worker': worker, 'current_user':current_user, 'msgs':msgs}
    
    return render(request, 'chat.html', context)

@login_required(login_url='login')
def update_msg(request, pk):
    
    worker = Worker.objects.get(id=pk)
    msg = request.POST.get('msg')
    current_user = request.user
    ChatMessage.objects.create(sender=current_user, receiver=worker, body=msg)
    # return HttpResponse(status=204, headers={'HX-Trigger':'msgChanged'})
    return redirect('chat', pk=pk)
    




