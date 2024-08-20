from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# rooms = [
#     {'id': 1, 'name': 'lets learn somthing'},
#     {'id': 2, 'name': 'lets learn nothing'},
#     {'id': 3, 'name': 'lets learn everything'},

# ]  


def home(request):
    q = request.GET.get('q','') 
    rooms=Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__contains=q) |
        Q(description__contains=q) |
        Q(host__username__contains=q))
    room_count = rooms.count()
    roommessages= Message.objects.all()
    
    topic = Topic.objects.all()
    return render(request, 'socialsite/home.html', {'rooms':rooms, 'topic':topic, 'room_count':room_count, 'roommessages':roommessages})

@login_required(login_url='/login')
def room(request, pk):
    room= None
    rooms = Room.objects.all()
    roommessages = None
    participants = None

    for i in rooms:
        if int(i.id) == int(pk):
            room = i
            roommessages = room.message_set.all().order_by('-created')
            participants = room.participants.all()
            participantNumber = participants.count()

            if request.method == 'POST':
                message = Message.objects.create(
                    user = request.user,
                    room = room,
                    body =  request.POST.get('body'),
                )
                room.participants.add(request.user)
                return redirect('room', pk=room.id)
    context = {'room':room, 'roommessages': roommessages, 'participants':participants,'participantNumber': participantNumber}
    return render(request, 'socialsite/room.html', context)

@login_required(login_url='/login')
def createroom(request):
    form = RoomForm()
    if request.method == 'POST':

        form = RoomForm(request.POST)
        # form = request.POST.copy()
        # form['host'] = request.user
        # form = RoomForm(form)
        
        # print(form)
        if form.is_valid():
            form = form.save(commit = False)
            form.host = request.user
            form.save()
            return redirect('home')
        return HttpResponse('Form not submitted')

    context = {'form':form}
    return render(request, 'socialsite/room_form.html', context)

@login_required(login_url='/login')
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('you are not allowed to delete this')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        # print(form)
        if form.is_valid():
            form.save()
            return redirect('home')
        return HttpResponse('Form not submitted')

    context={'form':form}
    return render(request, 'socialsite/updateroom.html', context)

@login_required(login_url='/login')
def delete(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'socialsite/delete.html', {'obj':room})

def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        username = username.lower()
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'No user')

        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is invalid or do not match')
    context ={'page': page}
    return render(request, 'socialsite/login_register.html', context)

def logoutuser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form  = UserCreationForm(request.POST)
        # registerform = form.copy()
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        return HttpResponse('error')
    return render(request, 'socialsite/login_register.html',{'page':page, 'form':form})


login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=message.room.id)
    return render(request, 'socialsite/delete.html', {'Obj': message})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = Room.objects.filter(host = user)
    topics = []
    # topics = user.room_set.all().topic
    for room in rooms:
        if room.topic in topics:
            pass
        else:
            topics.append(room.topic)
    

    message = Message.objects.filter(user = user)
    context = {'user':user, 'rooms':rooms,'roommessages': message,'topic': topics}
    return render(request, 'socialsite/profile.html', context)


@login_required(login_url='login')
def editProfile(request, pk):
    user = User.objects.get(id = pk)
    form=UserForm(instance = user)
    if request.method =='POST':
        form = UserForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            # return redirect('profile')
            return HttpResponse("saved succesfully")
        # password1 = request.POST.get('password1')
        # password2 = request.POST.get('password2')
        # if password1 != password2:
        #     return messages.error(request, "passwords don't match")
        # if len(password1) < 8:
        #     return messages.error(request, 'password too short')
        # user.username = username
        # user.set_password = password1
        # user.save()
        return messages.error(request, 'invalid email or username exists')
    context = {'form': form}
    return render(request, 'socialsite/editprofile.html', context )
