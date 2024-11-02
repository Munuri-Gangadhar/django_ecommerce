from django.shortcuts import render,redirect
from . models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm




def product(request,pk):
    product=Product.objects.get(id=pk)
    return render(request,'product.html',{'products':product})


def category_summary(request):
    categories=Category.objects.all()
    return render(request,'category_summary.html',{"categories":categories})

def category(request,foo):
    foo=foo.replace("-",' ')
    try:
        category=Category.objects.get(name=foo)
        products=Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products},{'category':category})

    except:
        messages.success(request,("The category does not exits"))
        return redirect('home')

def home(request):
    products=Product.objects.all()
    print(products)
    return render(request,'home.html',{'products':products})


def about(request):
    return render(request,'about.html',{})


def login_user(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You have been Logged In!"))
            return redirect('home')
        else:
            messages.success(request,("There was an error"))
            return redirect('login')
    else:
        return render(request,'login.html',{})

    return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out..Thanks for stopping by.."))
    return redirect('home')

def register_user(request):
    form=SignUpForm()
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']

            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You have Registered Successfully"))
            return redirect('update_user')
        else:
            messages.success(request,("Whoops! There was an problem occured"))
            return redirect('register')
    else:
        return render(request,'register.html',{'form':form})


def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        user_form=UpdateUserForm(request.POST or None,instance=current_user)

        if user_form.is_valid():
            user_form.save()
            
            login(request,current_user)

            messages.success(request,"User Has Been Updated")
            return redirect('home')
        return render(request,"update_user.html",{'user_form':user_form})
    
    else:
        messages.success(request,"You Must be logged in to Updated")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)  # Keeps user logged in after password change
                messages.success(request, "Your password has been changed.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
        
        return render(request, 'update_password.html', {'form': form})
    
    else:
        messages.error(request, "You must be logged in to update your password.")
        return redirect('home')


def update_info(request):
    if request.user.is_authenticated:
        current_user=Profile.objects.get(user__id=request.user.id)
        form=UserInfoForm(request.POST or None,instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request,"User Info Has Been Updated")
            return redirect('home')
        return render(request,"update_info.html",{'form':form})
    
    else:
        messages.success(request,"You Must be logged in to Updated")
        return redirect('home')


def search(request):
    pass
