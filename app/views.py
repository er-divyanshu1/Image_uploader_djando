from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth .decorators import login_required
from datetime import date


# Create your views here.

def index(request):

    if request.method=='POST':
        user= request.user
        suser=SUser.objects.get(user=user)
        file= request.FILES['file']
        date1 = date.today()
        UploadPhpto.objects.create(file=file, postdate=date1.today(),suser=suser)
        messages.success(request,'Congratulation ! your Photo successfully uploaded.')
    file = UploadPhpto.objects.all()
    data={'file':file,}

    return render (request,'index.html',data)

def u_login(request):
    if request.method=='POST' :
       uname = request.POST['email']
       pass1 = request.POST['pass']
       user= authenticate (request,username= uname, password=pass1)
       if user is not None:
            login(request,user)
            return redirect('index')
       else:
           messages.warning(request,'Somthig went Wrong.')
           return redirect('login')
    
    return render(request,"login.html")


def signup(request):
    error= ""
    if request.method=='POST' :
       fname = request.POST['first_name']
       lname = request.POST['last_name']
       email = request.POST['email']
       phone = request.POST['phone']
       gender = request.POST['gender']
       p1 = request.POST['pass1']
       p2 = request.POST['pass2']

       if p1 != p2:
            messages.warning(request,'Password is does not match.')
            return redirect('signup')
       elif User.objects.filter(username=email).exists():
           messages.warning(request,'Email allredy taken')
           return redirect('signup')
       else:
            try:
                user=User.objects.create_user(first_name=fname,last_name=lname, username=email,email=email, password=p1)
                SUser.objects.create(user=user, mobile=phone,gender=gender,)
                messages.success(request,'User registerd successfull.')
                return redirect('login')
            except:
                messages.warning(request,'Something  Wrong...')
    return render(request,'signup.html')

def logoutUser(request):
    logout(request)
    messages.warning(request,'You are logout')
    return redirect('index')


@login_required(login_url='login')
def profile(request):
    user1= request.user
    usr= SUser.objects.get(user=user1)
    data={'usr':usr,}
    return render(request,"profile.html",data)

@login_required(login_url='login')
def change_password(request):
    if request.method=='POST' :
       p1 = request.POST['pass1']
       p2 = request.POST['pass2']
       p3 = request.POST['pass3']
       try:
            u=User.objects.get(id=request.user.id)
            if p2 != p3:
                messages.warning(request,'Password and Confirm Password did not match.')
                return redirect('change_password')
                
            elif u.check_password(p1):
                u.set_password(p2)
                u.save()
                pass
                messages.success(request,'User new password  successfuly udated.')
                
            else:
                messages.warning(request,'User old password is wrong')
                return redirect('change_password')
       except:
            messages.warning(request,'Something  Wrong...')
    return render(request,"change_password.html")

def forget_pass_form(request):
    return render(request,'forget_pass_form.html')

@login_required(login_url='user_login')
def user_edit_profile(request):
    usr= request.user
    usr= SUser.objects.get(user=usr)
    data={'usr':usr,}
    if request.method=='POST' :
       fname = request.POST['first_name']
       lname = request.POST['last_name']
       phone = request.POST['phone']
       address = request.POST['address']
       age = request.POST['age']
       usr.user.first_name = fname
       usr.user.last_name = lname
       usr.mobile = phone
       usr.address = address
       usr.age= age
       try:
            usr.save()
            usr.user.save()
            
            
       except:
            messages.warning(request,'Something  Wrong...')
       try:
            img = request.FILES['img']
            usr.img = img
            usr.save()
       except:
            pass
       messages.success(request,' Your Profile Successfully Updated.')
       return redirect('profile',)
    return render(request,"user_edit_profile.html",data)


def image_detail(request,id):
    user1= request.user
    usr= SUser.objects.get(user=user1)
    photo=UploadPhpto.objects.get(id=id)
    cmt=Comments.objects.filter(photo=photo).order_by('-postdate')
    


    if request.method=='POST':
        user= request.user
        suser=SUser.objects.get(user=user)
        id=request.POST.get("id")
        comment= request.POST['comment']
        if comment=='':
            context ={'photo':photo,'usr':usr,'cmt':cmt}
        else:
            date1 = date.today()
            Comments.objects.create(comment=comment, postdate=date1.today(),suser=suser,photo=photo)
           
            messages.success(request,'Congratulation ! your comment successfully added.')

    context ={'photo':photo,'usr':usr,'cmt':cmt}
    print(context)
    return render(request, "image_details.html",context)

