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
    janitors = Janitor.objects.all().order_by('name')
    collectors = Collector.objects.all().order_by('name')
    vehicles = Vehicle.objects.all().order_by('name')
    trolleys = Trolley.objects.all().order_by('name')
    mcps = MCP.objects.all().order_by('name')
    areas = Area.objects.all().order_by('name')
    date_time = datetime.date.today()
    area_today = Area_Janitor.objects.filter(work_date = date_time)
    mcp_today_janitor = MCP_Janitor.objects.filter(work_date = date_time)
    trolley_today = Trolley_Janitor.objects.filter(work_date=date_time)
    mcp_today_collector = MCP_Collector.objects.filter(work_date=date_time)
    vehicle_today = Vehicle_Collector.objects.filter(work_date=date_time)
    
    vehicle_list=[] 
    for vehicle in vehicles:
        temp = {
            "id": vehicle.id,
            "name": vehicle.name,
            "collector": "Chưa giao",
        }
        if (vehicle_today.filter(vehicle = vehicle).exists()):
            temp["collector"] = vehicle_today.get(vehicle=vehicle).collector.name
        
        vehicle_list.append(temp)

        
    trolley_list=[]
    for trolley in trolleys:
        temp = {
            "id": trolley.id,
            "name": trolley.name,
            "janitor": "Chưa giao",
        }
        if (trolley_today.filter(trolley = trolley).exists()):
            temp["janitor"] = trolley_today.get(trolley=trolley).janitor.name
        
        trolley_list.append(temp)
    
    area_list = []
    
    for area in areas:
        temp = {
            "id": area.id,
            "name": area.name,
            "janitor": "",
        }
        if (area_today.filter(area = area).exists()):
            tmp = area_today.filter(area=area)
            temp["janitor"] = ', '.join(area.janitor.name for area in tmp)
        else:
            temp["janitor"] = "Chưa giao"
        area_list.append(temp)
        
    mcp_list = []
    
    for mcp in mcps:
        temp = {
            "id": mcp.id,
            "name": mcp.name,
            "capacity": mcp.capacity,
            "janitor": "",
            "collector": "",
        }
        if (mcp_today_janitor.filter(mcp = mcp).exists()):
            tmp = mcp_today_janitor.filter(mcp = mcp)
            temp["janitor"] = ', '.join(mcp.janitor.name for mcp in tmp)
        else:
            temp["janitor"] = "Chưa giao"
            
        if (mcp_today_collector.filter(mcp = mcp).exists()):
            tmp = mcp_today_collector.filter(mcp = mcp)
            temp["collector"] = ', '.join(mcp.collector.name for mcp in tmp)
        else:
            temp["collector"] = "Chưa giao"    
            
        mcp_list.append(temp)
    
    
    context ={'janitors': janitors, 'collectors': collectors, 'vehicles': vehicles,
              'trolleys': trolleys, 'mcps': mcps, 'areas': areas, 'date': date_time.strftime("%Y-%m-%d"),
              'vehicle_list':vehicle_list, 'trolley_list':trolley_list, "area_list": area_list, "mcp_list": mcp_list}
    
    return render(request, 'home.html', context)

@login_required(login_url='login')
def collector_page(request, pk, date_time):
    collector = Collector.objects.get(id = pk)
    date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d').date()
    is_checked = True
    if(date_time <= datetime.date.today()):
        is_checked = True
    else:
        is_checked = False
    
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
               'used_mcp_count': len(used_mcp), 'ori': ori, 'dest': dest, 'waypoint': waypoint, "is_checked": is_checked}
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
def delete_collector_vehicle(request, pk, date_time):

    if request.method == "POST":
        date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d')
        collector = Collector.objects.get(id = pk)
        chosen_vehicle = Vehicle.objects.get(id = request.POST.get('delete_vehicle'))
        Vehicle_Collector.objects.filter(work_date=date_time, collector = collector, vehicle = chosen_vehicle).delete()

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
def update_collector_mcp(request, pk, date_time):

    if request.method == "POST":
        date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d')
        collector = Collector.objects.get(id = pk)
        current_mcp= MCP.objects.get(id = request.POST.get('currentmcp'))
        chosen_mcp= MCP.objects.get(id = request.POST.get('chosenmcp'))
        
        MCP_Collector.objects.filter(collector = collector, work_date = date_time, mcp = current_mcp ).update(mcp=chosen_mcp)
        return redirect('collector', pk = pk, date_time = date_time.strftime("%Y-%m-%d"))
    
@login_required(login_url='login')
def janitor_page(request, pk, date_time):
    janitor = Janitor.objects.get(id = pk)
    date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d').date()
    is_checked = True
    if(date_time <= datetime.date.today()):
        is_checked = True
    else:
        is_checked = False
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
               'area_all': Area.objects.all(), 'used_area':used_area, 'map_choice': map_choice, "is_checked": is_checked}
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
def delete_janitor_area(request, pk, date_time):

    if request.method == "POST":
        date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d')
        janitor = Janitor.objects.get(id = pk)
        chosen_area = Area.objects.get(id = request.POST.get('delete_area'))

        Area_Janitor.objects.filter(janitor=janitor, work_date=date_time, area =chosen_area).delete()
        return redirect('janitor', pk = pk, date_time = date_time.strftime("%Y-%m-%d"))
    
@login_required(login_url='login')
def delete_janitor_mcp(request, pk, date_time):

    if request.method == "POST":
        date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d')
        janitor = Janitor.objects.get(id = pk)
        chosen_mcp = MCP.objects.get(id = request.POST.get('delete_mcp'))

        MCP_Janitor.objects.filter(janitor=janitor, work_date=date_time, mcp =chosen_mcp).delete()
        return redirect('janitor', pk = pk, date_time = date_time.strftime("%Y-%m-%d"))
    
@login_required(login_url='login')
def delete_janitor_trolley(request, pk, date_time):

    if request.method == "POST":
        date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d')
        janitor = Janitor.objects.get(id = pk)
        chosen_trolley = Trolley.objects.get(id = request.POST.get('delete_trolley'))

        Trolley_Janitor.objects.filter(janitor=janitor, work_date=date_time, trolley = chosen_trolley).delete()
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
    




