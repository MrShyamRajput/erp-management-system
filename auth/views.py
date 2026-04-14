from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)

        user = authenticate(request, username="shyam", password=password)
        print(user)

        if user is not None:
            login(request, user)
            return redirect("/dashboard")
            print("reditecting")
        else:
            messages.error(request, "Invalid Email or password")
    
    return render(request, "auth/login.html")


User = get_user_model()


@login_required
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        role = request.POST.get("role")
        password = request.get("password")
        confirn_password = request.get("confirm_password")
        
        if password != confirn_password:
            messages.error(request, "Password do not match")
            return redirect("register")
            
        if User.objects.filter(email=email).exist():
            messages.error(request, "User already exists")
            return redirect(register)

        user = User.objects.create(username=email,
        email=email,
        password=password
        )

        user.first_name = name
        user.role = role
        user.save()
        messages.success("User Created successfully")

        return redirect("dashboard")
    return render(request, "auth/register.html")            



