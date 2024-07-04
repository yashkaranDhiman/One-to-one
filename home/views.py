from django.db.utils import IntegrityError  # Import IntegrityErrorfrom django.contrib import messages
from .forms import ProfileEditForm
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from django.db.models import Max  # Import Max to get the latest message
from django.db.models import Max, OuterRef, Subquery
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import json

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user.profile
        friends = user.friends.all()
        # Subquery to get the latest message for each friend
        latest_messages = ChatMessages.objects.filter(
            msg_sender=OuterRef('profile'),
            msg_receiver=user
        ).order_by('-created').values('body')[:1]

        # Annotate the friends queryset with the latest message subquery
        friends = friends.annotate(latest_message=Subquery(latest_messages))
        context = {
            "user": user,
            "friends": friends,
        }
        return render(request, "home/index.html", context)
    else:
        return redirect("register")

def friend(request,pk):
    if request.user.is_authenticated:
        user = request.user.profile
        specific_friend = Friend.objects.get(id=pk)
        friend_profile = Profile.objects.get(id=specific_friend.profile.id)
        all_chat = ChatMessages.objects.all()
        rec_chats = ChatMessages.objects.filter(msg_sender=friend_profile,msg_receiver=user)
        if request.method == "POST":
            msg_body = request.POST.get('mssg')
            msg_sender = request.user.profile
            msg_receiver = Profile.objects.get(id=specific_friend.profile.id)
            message = ChatMessages(body=msg_body,msg_sender=msg_sender,msg_receiver=msg_receiver)
            message.save()
        context = {'specific_friend':specific_friend,'all_chat':all_chat,"num":rec_chats.count()}
        return render(request,"home/chat_page.html",context)
    else:
        return redirect("register")

def all_friend(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            get_query = request.POST.get('srch')
            # Filter by 'name' and 'user' fields without attempting to filter by 'id'
            all_friends = Profile.objects.filter(Q(name__icontains=get_query))
        else:
            all_friends = Profile.objects.all()
        context = {"all_friends": all_friends}
        return render(request, 'home/all_friends.html', context)
    else:
        return redirect("register")

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request,"home/signup.html")
    else:
        return redirect("register")

def sentMessage(request,pk):
    if request.user.is_authenticated:
        user = request.user.profile
        friend = Friend.objects.get(profile_id=pk)
        friend_profile = Profile.objects.get(id=friend.profile.id)
        data = json.loads(request.body)
        New_chat= data['msg']
        print(New_chat)
        new_chat_message = ChatMessages.objects.create(body=New_chat,msg_sender=user,msg_receiver=friend_profile)
        return JsonResponse(new_chat_message.body,safe=False)
    else:
        return redirect("register")

def recerivedMessges(request,pk):
    if request.user.is_authenticated:
        user = request.user.profile
        friend = Friend.objects.get(profile_id=pk)
        friend_profile = Profile.objects.get(id=friend.profile.id)
        arr = []
        chats = ChatMessages.objects.filter(msg_sender=friend_profile,msg_receiver=user)
        for chat in chats:
            arr.append(chat.body)
        return JsonResponse(arr,safe=False)
    else:
        return redirect("register")

def profile_page(request,pk):
    if request.user.is_authenticated:
        my_profile = Profile.objects.get(id=pk)
        user_id  = request.user.profile.id
        my_friends = my_profile.friends.count()
        # my_followers = my_profile.followers.count()
        
        context = {'pro':my_profile,"my_frnd":my_friends,"user_id":user_id}
        return render(request,'home/profile.html',context)
    else:
        return redirect("register")

def edit_profile(request, pk):
    if request.user.is_authenticated:
        to_edit = Profile.objects.get(id=pk)
        if request.method == 'POST':
            form = ProfileEditForm(request.POST, request.FILES, instance=to_edit)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = ProfileEditForm(instance=to_edit)
        context = {'to_edit': to_edit, 'form': form}
        return render(request, 'home/edit_profile.html', context)
    else:
        return redirect("register")

def get_unseen_message_count(request, friend_id):
    if request.user.is_authenticated:
        user = request.user.profile
        friend = Friend.objects.get(id=friend_id)
        friend_profile = Profile.objects.get(id=friend.profile.id)

        # Calculate the count of unseen messages
        unseen_count = ChatMessages.objects.filter(
            msg_sender=friend_profile,
            msg_receiver=user,
            seen=False
        ).count()

        # Return the count as JSON response
        return JsonResponse({'unseen_count': unseen_count})
    else:
        return redirect("register")


def signup_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        form = User(request.POST)
        if password == password2:
            try:
                myuser = User.objects.create_user(username=username, password=password, email=email)
                new_user_profile = Profile(user=myuser, name=username)
                new_user_friend = Friend(profile=new_user_profile)
                new_user_profile.save()
                new_user_friend.save()
                login(request, myuser)
                messages.success(request, f"Welcome {myuser.username}")  # Changed 'user' to 'myuser'
                return redirect("/")
            except IntegrityError:
                messages.success(request, "This username already exists")
        else:
            messages.error(request, "Passwords do not match")
            return render(request, 'home/signup.html', {'form': form})
    return render(request, 'home/signup.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}")
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'home/login.html')

