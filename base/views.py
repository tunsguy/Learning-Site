from django.shortcuts import render,redirect
from . models import Topic,Room,Message,User
from . forms import RoomForm,RegisterForm,UpdateForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    q= request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:3]
    message_room = Message.objects.filter(room__topic__name__icontains=q)
    room_count = rooms.count()
    context = {"rooms":rooms,"topics":topics,"room_count":room_count,"message_room":message_room}
    return render(request,"base/home.html",context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    message_room = room.message_set.all()
    participants = room.participants.all()
    if request.method =="POST":
        message = Message.objects.create(
            user = request.user,
            room=room,
            body = request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room",pk=room.id)
    context = {"room":room,"message_room":message_room,"participants":participants}
    return render(request,"base/room.html",context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            image = request.FILES.get("image"),
            host = request.user,
            topic= topic,
            name = request.POST.get("name"),
            description = request.POST.get("description")
        )
        return redirect("home")
    return render(request,"base/create-room.html",{"form":form,"topics":topics})


@login_required(login_url="login")
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.image = request.FILES.get("image")
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()   
        return redirect("room",pk=room.id)
    return render(request,"base/create-room.html",{"form":form,"topics":topics,"room":room})


@login_required(login_url="login")
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("/")
    return render(request,"base/delete.html",{"obj":room})


@login_required(login_url="login")
def deletemessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.method == "POST":
        message.delete()
        return redirect("room",pk=message.room.id)
    return render(request,"base/delete.html",{"obj":message})

def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,"User does not exist")
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Username OR Password does not exist")
    return render(request,"base/login_register.html",{"page":page})

def logoutPage(request):
    logout(request)
    return redirect("/")

def registerPage(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"An error occured in during registration")
    return render(request,"base/login_register.html",{"form":form})


def profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    message_room = user.message_set.all()
    context = {"user":user,"rooms":rooms,"topics":topics,"message_room":message_room}
    return render(request,"base/profile.html",context)


def UpdateUser(request):
    user = request.user
    form = UpdateForm(instance=user)
    if request.method == "POST":
        form = UpdateForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=user.id)
    return render(request,"base/edit-user.html",{"form":form})


def topics(request):
    q= request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,"base/topics.html",{"topics":topics})

def activity(request):
    message_room = Message.objects.all()
    return render(request,"base/activity.html",{"message_room":message_room})