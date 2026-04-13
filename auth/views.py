from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login


# Create your views here.
def login_page(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        user=authenticate(request,username=email,password=password)

        if user is not None:
            login(request, user)  

            

            if user.is_superuser:
                return redirect() #added
    return render(request,"auth/login.html")