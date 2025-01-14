from django.shortcuts import render,redirect
from django.http import HttpResponse
from vege.models import Receipe,UserSession
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    queryset = Receipe.objects.all()
    context = { 'receipes':queryset}
    return render(request,'home.html',context)


@login_required(login_url="/login/")
def receipes(request):
    if request.method == "POST":
        data = request.POST
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")
        receipe_count = data.get("receipe_view_count")
        receipe_image = request.FILES.get('receipe_image')
        Receipe.objects.get_or_create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image,
            receipe_count =receipe_count 
            )
        return redirect('/receipes/')
    queryset = Receipe.objects.all()
    if request.GET.get('query'):
        queryset = queryset.filter(receipe_name__icontains=request.GET.get('query'))

    context = { 'receipes':queryset}
    return render(request,'receipes.html',context)

def update_receipe(request,r_id):
    queryset = Receipe.objects.get(id=r_id)
    if request.method == "POST":
        data = request.POST
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")
        receipe_image = request.FILES.get('receipe_image')
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        if receipe_image:
            queryset.receipe_image = receipe_image
        queryset.save()
        return redirect('/receipes/')
    context = {'receipe':queryset}
    return render(request,'update_receipes.html',context)


def delete_receipe(request,r_id):
    queryset = Receipe.objects.get(id=r_id)
    queryset.delete()
    return redirect('receipes.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if  not User.objects.filter(username=username).exists:
            messages.error(request,'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username=username , password=password)
        
        if user is None:
            messages.error(request,"Invalid Password")
            return redirect('/login/')
        else:
            existing_session = UserSession.objects.filter(user=user).first()
            if existing_session:
                print("++++==",existing_session)
                messages.error(request,"You are already login from another device.")
                return redirect('/login/')
            login(request,user)
            UserSession.objects.create(user=user,session_key=request.session.session_key)
            messages.info(request,f"{user} logged in succesfully.")
            return redirect('/receipes/')
    return render(request,'login.html')

def logout_user(request):
    if request.user.is_authenticated:
        # Delete the user's session record
        UserSession.objects.filter(user=request.user).delete()
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect('/login/')


def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request,'Username already taken')
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save()
        messages.info(request,'Account created successfully.')
        return redirect('/register/')
    return render(request,'register.html')